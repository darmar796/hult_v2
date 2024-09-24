from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
# from .models import Member, InputForm, Player, Game
# from .models import Member, InputForm, Player, Game, AddReservation
from .models import InputForm, Player, Game, AddReservation
from datetime import datetime, date
# import pandas as pd
import json
from .google_sheets_example import GSheetsLogger
from .sunset_example import HultSun
# import numpy as np
import pandas as pd
import uuid
# from autofill_websites.helpers.google_sheets_example import GSheetsLogger
from django.contrib.auth.decorators import login_required

def members(request):
  mymembers = Member.objects.all().values()
  template = loader.get_template('all_members.html')
  context = {
      'mymembers': mymembers,
      }
  return HttpResponse(template.render(context, request))

def players(request, game_id):
  game = Game.objects.get(id=game_id)
  game.players.set(Player.objects.filter(game_id=game_id))
  currentplayers = game.players.all().values() # get players from game with game_id

  if request.user.is_authenticated:
      template = loader.get_template('list_players_loggedin.html')
  else:
      template = loader.get_template('list_players.html')
  context = {
      'currentplayers': currentplayers,
      'game_id': game_id,
      }
  return HttpResponse(template.render(context, request))


def details(request, id):
  mymember = Member.objects.get(id=id)
  template = loader.get_template('details.html')
  context = {
      'mymember': mymember,
      }
  return HttpResponse(template.render(context, request))

# def main(request):
#     template = loader.get_template('main.html')
#     return HttpResponse(template.render())

def short_day(day):
    map = {'Monday': 'Mon',
        'Tuesday': 'Tue',
        'Wednesday': 'Wed',
        'Thursday': 'Thu',
        'Friday': 'Fri',
        'Saturday': 'Sat',
        'Sunday': 'Sun'}

    return map[day]

def main(request):

    gsheets_service_key = "/home/darmar796/autofill_websites/autofill_websites/hult-auto-reservation-1a0360021964.json"
    main_log_gsheet = "Hult Reservations"

    logger = GSheetsLogger(service_key=gsheets_service_key)
    logger.open_spreadsheet(main_log_gsheet)

    # bot's log
    logger.select_sheet(2)
    df_log_bot = logger.get_log()

    # manual log
    logger.select_sheet(3)
    df_log_manual = logger.get_log()
    # filter manual log from today's date onwards
    todays_date = date.today().isoformat()  # grab today's date

    # grab dates from today onwards (e.g. do not display past manual reservations)
    filtered_df = df_log_manual.loc[df_log_manual['date'] >= todays_date]

    # bot + manual reservations combined in one data frame
    df_log = pd.concat([df_log_bot, filtered_df])

    # arange by date
    df_log['date'] = pd.to_datetime(df_log['date'])
    df_log = df_log.sort_values(by='date')

    # fix the formatting from datetime to string
    df_log['date'] = df_log['date'].dt.strftime('%Y-%m-%d')

    # shorten the day to 3 letters
    df_log['day'] = df_log['day'].apply(short_day)

    # every row create Game model, this will hold list of players
    # for game_id in df_log['id']:
    for game_id in df_log['uuid']:

        if not Game.objects.filter(id=game_id).exists():
            game_to_add = Game(id=game_id)
            game_to_add.save()
            for i in range(15):
                # initialize 15 open spots
                player_to_add = Player(name='---JOIN---', game_id=game_id, user_id=None)
                player_to_add.save()


    # parsing the DataFrame in json format.
    json_records = df_log.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    context = {'d': data}

    if request.user.is_authenticated:
        template = loader.get_template('table_loggedin.html')
    else:
        template = loader.get_template('table.html')

    return HttpResponse(template.render(context, request))

def testing(request):
  mymembers = Member.objects.all().values()
  template = loader.get_template('template.html')
  context = {
    'mymembers': mymembers,
  }
  return HttpResponse(template.render(context, request))

def about(request):
  if request.user.is_authenticated:
      context = {'user': request.user}
      template = loader.get_template('about_loggedin.html')
      return HttpResponse(template.render(context,request))

  else:
      template = loader.get_template('about.html')
      return HttpResponse(template.render())


@login_required(login_url="/accounts/login/")
def input_view(request, game_id):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            # Save the data to the database
            name = form.cleaned_data['name']
            player_to_add = Player(name=name, game_id=game_id, user_id=request.user.id)
            player_to_add.save()
            # game.players.set(Player.objects.all())

            # Redirect the user to another page
            return HttpResponseRedirect(f'/games/{game_id}/')  # need to go to game_id
    else:
        form = InputForm()

    template = loader.get_template('input.html')
    context = {'form': form,
                'game_id': game_id}

    return HttpResponse(template.render(context, request))

@login_required(login_url="/accounts/login/")
def change_player_name(request, game_id, player_id):
    game_to_modify = Game.objects.get(id=game_id)
    player_to_modify = game_to_modify.players.get(id=player_id)

    player_name = player_to_modify.name
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():

            # print(f"USER1:::::::::::::::::: {request.user.id}")
            # print(f"USER2:::::::::::::::::: {player_to_modify.user_id}")
            # print(f"{request.user.id == player_to_modify.user_id}")
            # print(f"{player_to_modify.user_id == 'None'}")
            # print(f"{player_to_modify.user_id is None}")

            if request.user.id == player_to_modify.user_id or player_to_modify.user_id is None:
                # Save the data to the database
                name = form.cleaned_data['name']
                player_to_modify.name = name
                player_to_modify.user_id = request.user.id
                player_to_modify.save()
            # game.players.set(Player.objects.all())

            # Redirect the user to another page
            return HttpResponseRedirect(f'/games/{game_id}/')  # need to go to game_id
    else:
        form = InputForm()

    template = loader.get_template('change_player.html')
    context = {'form': form,
                'game_id': game_id,
                'player_id': player_id,
                'player_name': player_name}

    return HttpResponse(template.render(context, request))


@login_required(login_url="/accounts/login/")
def empty_player_name(request, game_id, player_id):

    if request.user.is_authenticated:
        # Do something for authenticated users.
        game_to_modify = Game.objects.get(id=game_id)

        # print(f"EMPTY USER ID1::::::::::::::::::::::::: {request.user.id}")

        # print(f"EMPTY USER ID2::::::::::::::::::::::::: {game_to_modify.players.get(id=player_id).user_id}")

        # print(f"{request.user.id == game_to_modify.players.get(id=player_id).user_id}")
        # print(f"{game_to_modify.players.get(id=player_id).user_id is None}")
        # print(type(request.user.id))
        # print(type(game_to_modify.players.get(id=player_id).user_id))

        if request.user.id == game_to_modify.players.get(id=player_id).user_id or game_to_modify.players.get(id=player_id).user_id is None :
            player_to_modify = game_to_modify.players.get(id=player_id)
            player_to_modify.name = '---JOIN---'
            player_to_modify.user_id = None
            player_to_modify.save()
        return HttpResponseRedirect(f'/games/{game_id}/')  # need to go to game_id
    else:
        # Do something for anonymous users.
        return HttpResponseRedirect('/accounts/login/')




@login_required(login_url="/accounts/login/")
def modify_player(request, game_id, player_id):
    game_to_modify = Game.objects.get(id=game_id)
    player_to_modify = game_to_modify.players.get(id=player_id)
    player_name = player_to_modify.name

    if player_name == '---JOIN---':
        return HttpResponseRedirect(f'/games/{game_id}/{player_id}/input')

    template = loader.get_template('modify_player.html')
    context = {'game_id': game_id,
               'player_id': player_id,
                'player_name': player_name}

    return HttpResponse(template.render(context, request))


@login_required(login_url="/accounts/login/")
def add_reservation(request):
    if request.method == 'POST':
        form = AddReservation(request.POST)
        if form.is_valid():

            # Figure out sunset time
            hult_sun = HultSun()
            local_sunset = hult_sun.get_sunset_from_date(form.cleaned_data['date'].isoformat())
            local_sunset = local_sunset.time().strftime(hult_sun.fmt)

            # Add reservation to list of reservations
            # Currently data is extracted from a google sheet

            # this needs to be added to via form to Google Sheet
            # note it's important to add it to all 3 sheets
            # this is because the automated bot also touches those sheets
            # and uses the sheet index [0] as the true source of information
            # and automatically adjusts sheet index [1] and sheet index [2]
            # ultimately the main web page creates the list from the sheet
            # index [2]
            # other idea is to maintain sheet index [3] - Manual List Of Reservations to keep it separate from the bot's logs
            gsheets_service_key = "/home/darmar796/autofill_websites/autofill_websites/hult-auto-reservation-1a0360021964.json"
            main_log_gsheet = "Hult Reservations"

            logger = GSheetsLogger(service_key=gsheets_service_key)
            logger.open_spreadsheet(main_log_gsheet)
            logger.select_sheet(3) # sheet index [3]

            df_log = pd.DataFrame()
            df_log['date'] = [form.cleaned_data['date']]
            df_log['day'] = [form.cleaned_data['date'].strftime('%A')] # ['Wednesday']
            df_log['time'] = [form.cleaned_data['time'].strftime(hult_sun.fmt)]
            df_log['end_time'] = [form.cleaned_data['end_time'].strftime(hult_sun.fmt)]
            df_log['status'] = ['Booked']
            df_log['name'] = ['Dario Martinovic']
            df_log['email'] = ['dario.vivamus@gmail.com']
            df_log['phone'] = ['7743187224']
            df_log['sunset'] = [local_sunset]
            df_log['timestamp'] = [datetime.now().astimezone(hult_sun.local_tz).isoformat()]
            df_log['uuid'] = uuid.uuid4().hex

            logger.update_log(df_log, overwrite=False)

            # Redirect the user to another page
            return HttpResponseRedirect('/games/')
    else:
        form = AddReservation()

    template = loader.get_template('add_reservation.html')
    context = {'form': form}

    return HttpResponse(template.render(context, request))



# def Table(request):

#     # gsheets_service_key = "/home/darmar796/autofill_websites/autofill_websites/hult-auto-reservation-1a0360021964.json"
#     # main_log_gsheet = "Hult Reservations"

#     # logger = GSheetsLogger(service_key=gsheets_service_key)
#     # logger.open_spreadsheet(main_log_gsheet)
#     # logger.select_sheet(0)
#     # df_rb = logger.get_log()

#     df_log = pd.DataFrame()
#     df_log['date'] = ['2024-3-17']
#     df_log['day'] = ['Wednesday']
#     df_log['time'] = ['6:00 pm']
#     df_log['sunset'] = ['7:01 pm']
#     df_log['status'] = ['Booked']
#     df_log['name'] = ['Dario Martinovic']
#     df_log['email'] = ['dario.vivamus@gmail.com']
#     df_log['phone'] = ['7743187224']


#     # parsing the DataFrame in json format.
#     json_records = df_log.reset_index().to_json(orient ='records')
#     data = []
#     data = json.loads(json_records)
#     context = {'d': data}

#     template = loader.get_template('table.html')

#     return HttpResponse(template.render(context, request))