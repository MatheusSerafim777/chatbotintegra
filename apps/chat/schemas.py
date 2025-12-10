from ninja import Schema


class ChatSchema(Schema):
    mensagem: str
    stream: bool = False
    id_mensagem_pai: int | None = None
    id_conversa: int | None = None


class CurtirMensagemSchema(Schema):
    curtido: bool | None
