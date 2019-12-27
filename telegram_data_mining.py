from telethon import TelegramClient, events
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.messages import GetMessagesViewsRequest
from telethon.tl.types import InputMessagesFilterPhotos
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from telethon.tl.functions.messages import AddChatUserRequest

from tqdm import tqdm
import asyncio

api_id = 'YOUR API ID'
api_hash = 'YOUR API HASH HERE'
client = TelegramClient('anon', api_id, api_hash)


'''
To perform these programs you need to be the member of the group you are parsing

1) Get chats - gets all you chats and writes it in a txt file
2) Get user photos - downloads all photos from any telegram group. All you have to do is to write the Group name (Of course you need to me a member of that group)
3) Get usernames - gets the usernames of all members of a group.
4) Get_Messages - gets all the messages in a group. Gets 2 parametrs( numbers of messages, group_name)
'''

async def get_chats(client,filename):
	with open(filename,'w',encoding = 'utf-8') as file:
		async for dialog in client.iter_dialogs():
			file.write('{}:{}\n'.format(dialog.name,dialog.id))
			print(dialog.name, 'has ID', dialog.id)


async def get_users_photos():
	all_directories = os.listdir()
	if 'user- photos' not in all_directories:
		os.mkdir('user- photos')
	is_phone = False
	numbersss = False
	is_username = False
	folder_created = False
	async for dialog in client.iter_dialogs():
	    if dialog.name == 'ICE FAMILY':
	    	existing = [name for name in os.listdir(".") if os.path.isdir(name)]
	    	print(existing)
	    	print('found')
	    	async for user in client.iter_participants(dialog):
	    		counter = 0
	    		if (user.first_name not in existing) and (user.username) not in existing and (user.phone) not in existing:
	    			print(user.first_name)
	    			try:
		    			os.mkdir('user- photos/{}'.format(user.first_name))
		    			folder_created = True
		    		except Exception as e:
		    			print('1st exception')
		    			if user.username:
		    				os.mkdir('user- photos/{}'.format(user.username))
		    				is_username = True
		    			elif user.phone:
		    				os.mkdir('user- photos/{}'.format(user.phone))
		    				is_phone = True
		    			else:
		    				is_number = random.randint(0,10000)
		    				numbersss = True
		    				os.mkdir('user- photos/{}'.format(is_number))

		    		async for photo in client.iter_profile_photos(user):
		    			try:
		    				counter+=1
		    				if is_username:
		    					with open('user- photos/{}/{}.jpg'.format(user.username,photo.id), 'wb') as fd:
								    async for chunk in client.iter_download(photo):
								        fd.write(chunk)
								        print("written  ",counter)
		    				elif is_phone:
		    					with open('user- photos/{}/{}.jpg'.format(user.phone,photo.id), 'wb') as fd:
								    async for chunk in client.iter_download(photo):
								        fd.write(chunk)
								        print("written  ",counter)
			    			elif numbersss:
			    				with open('user- photos/{}/{}.jpg'.format(is_number,photo.id), 'wb') as fd:
								    async for chunk in client.iter_download(photo):
								        fd.write(chunk)
								        print("written  ",counter)

			    			elif folder_created:
				    			with open('user- photos/{}/{}.jpg'.format(user.first_name,photo.id), 'wb') as fd:
								    async for chunk in client.iter_download(photo):
								        fd.write(chunk)
								        print("written  ",counter)
		    			except Exception as e:
		    				print(e)
		    				await asyncio.sleep(10)
		    		is_phone = False
		    		is_username = False
		    		numbersss = False
		    		folder_created = False


async def get_usernames(group_name):
	with open(f"{group_name}.txt",'w',encoding='utf-8') as file:
	    async for dialog in client.iter_dialogs():
	    	if dialog.name == group_name:
	    		print('found')
	    		async for user in client.iter_participants(dialog):
	    			if user.username:
	    				file.write('@{}\n'.format(user.username))
		    	print("finished")
		    else:
		    	print("The chat is not found")

async def get_phone_numbers(filename,group_name):
    me = await client.get_me()
    print(me.stringify())

    username = me.username
    print(username)
    print(me.phone)
    with open(f"{filename}.txt",'w',encoding='utf-8') as file:
	    async for dialog in client.iter_dialogs():
	    	if dialog.name == group_name:
	    		print('found')
	    		counter = 0
		    	async for user in client.iter_participants(dialog):
		    		if user.phone:
		    			file.write(user.first_name + ":" + user.phone + '\n')
		    	print("finished")


async def get_messages(number,chat_name):
	'''
	To do:
	1) To be able to get photos
	2) Forwands, voice messages, videos
	'''
	async for dialog in client.iter_dialogs():
	    	if dialog.name == chat_name:
	    		print('found')
	    		with open("{}messages.txt".format(chat_name),'w',encoding = 'utf-8') as file:
		    		messages = await client.get_messages(dialog, number)
		    		for message in tqdm(messages):
		    			if message.message:
			    			file.write(message.message + '/////')
			    			print('Successfully written')
			    			await  asyncio.sleep(0.1)

with client:
    client.loop.run_until_complete(get_chats())
