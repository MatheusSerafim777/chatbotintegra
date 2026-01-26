export * from "./djangoForm";

type FileField = {
    name: string;
    url: string;
}

export type Documento = {
    id: number;
    nome: string;
    arquivo: FileField;
    status: 'pendente' | 'processando' | 'processado';
    tipo: 'legislacao' | 'manual';
}

export type Usuario = {
    id: number;
    name: string;
    email: string;
    is_staff: boolean;
}

export type Conversa = {
    id: number;
    nome: string;
}

export type PerguntaCanonica = {
    id: number;
    pergunta: string;
    embedding: string;
    resposta: string;
}