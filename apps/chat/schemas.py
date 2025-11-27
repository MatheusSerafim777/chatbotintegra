from ninja import Schema


class ChatSchema(Schema):
    mensagem: str
    stream: bool = False
    id_mensagem_pai: str | None = None
    id_conversa: str | None = None