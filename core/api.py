from ninja import NinjaAPI

api = NinjaAPI()


api.add_router('', 'chat.api.chat_router')
