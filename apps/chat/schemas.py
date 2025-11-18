from ninja import Schema


class ChatSchema(Schema):
    mensagem: str
    stream: bool = False
