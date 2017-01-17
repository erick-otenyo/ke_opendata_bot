import asyncio

import telepot
import telepot.aio
from aiohttp import ClientSession
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

i = u'\u2139\ufe0f'
smile = u'\U0001f600'
sorry = u'\U0001f625'
ds = u'\U0001f4cc'
cs = u'\U0001f4ca'
sh = u'\U0001f30d'
async def search_data(text, page=1):
	url = "http://opendata.arcgis.com/api/v2/datasets"
	params = {
		'q': text,
		'page[number]': page,
		'filter[tags]': 'kenya',
	}
	async with ClientSession() as session:
		async with session.get(url, params=params) as resp:
			resp = await resp.json()
			return resp


async def get_file(id):
	url = "http://opendata.arcgis.com/datasets/" + id
	filename = id
	async with ClientSession() as session:
		async with session.get(url) as resp:
			resp = await resp.read()
			with open(filename, 'wb') as f:
				f.write(resp)
			return filename


async def opendata(msg):
	content_typ, chat_type, chat_id = telepot.glance(msg)
	print(chat_id)
	if content_typ != 'text':
		return
	command = msg['text'].lower()
	if command == "/start":
		await bot.sendMessage(chat_id,
							  'Welcome to Kenya Open Data. To find data, send me the title of the dataset', )
	elif command == 'i':
		markup = InlineKeyboardMarkup(inline_keyboard=[
			[dict(text='Telegram URL', url='https://core.telegram.org/')],
			[InlineKeyboardButton(text='Callback - show notification', callback_data='notification')],
			[dict(text='Callback - show alert', callback_data='alert')],
			[InlineKeyboardButton(text='Callback - edit message', callback_data='edit')],
			[dict(text='Switch to using bot inline', switch_inline_query='initial query')],
		])
		
		global message_with_inline_keyboard
		message_with_inline_keyboard = await bot.sendMessage(chat_id, 'Inline keyboard with various buttons',
															 reply_markup=markup)
	else:
		await bot.sendMessage(chat_id, "Searching...")
		r = await search_data(msg['text'])
		data = r['data']
		if data:
			for item in data:
				id = item['id']
				attr = item['attributes']
				title = attr['title']
				desc = attr['description']
				content = attr['content']
				print(content)
				reply = "{0} <b>Dataset title:</b>\n{1}\n\n{2} <b>Description:</b>\n{3} ".format(i,title,ds,desc)
				inline_keyboard = [
					[InlineKeyboardButton(text='{0} Download CSV'.format(cs), callback_data="csv" + id)],
				]
				if content == "spatial dataset":
					inline_keyboard.append([InlineKeyboardButton(text='{0} Download shp'.format(sh), callback_data="shp" + id)])
				markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
				
				await bot.sendMessage(chat_id, reply, reply_to_message_id=msg['message_id'], reply_markup=markup,parse_mode='HTML')
		else:
			await bot.sendMessage(chat_id, "My Spiders cant find any dataset matching your query..{0}".format(sorry))
			await bot.sendMessage(chat_id, "Either the dataset is not yet on www.opendata.go.ke, or they are hungry and went to fish some bugs..{0}".format(smile))


async def on_callback_query(msg):
	query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
	chat_id = msg["message"]['chat']['id']
	if data.startswith("shp"):
		resp = await bot.answerCallbackQuery(query_id, )
		if resp == True:
			fn = data[3:] + "." + "zip"
			await bot.sendMessage(chat_id, "Getting shapefile....")
			file = await get_file(fn)
			await bot.sendDocument(chat_id, open(file, 'rb'))
	if data.startswith("csv"):
		resp = await bot.answerCallbackQuery(query_id, )
		if resp == True:
			fn = data[3:] + "." + "csv"
			await bot.sendMessage(chat_id, "Getting csv....")
			get_f = await get_file(fn)
			file = open(get_f,'rb')
			await bot.sendDocument(chat_id, file)


bot = telepot.aio.Bot("272125870:AAEXTFGM3haMsU_39QGAsi3hh3q1dOLvZYI")
answerer = telepot.aio.helper.Answerer(bot)
loop = asyncio.get_event_loop()
loop.create_task(bot.message_loop({'chat': opendata,
								   'callback_query': on_callback_query
								   }))
print('Listening ...')

loop.run_forever()
