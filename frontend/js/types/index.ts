export * from "./djangoForm";

type FileField = {
    name: string;
    url: string;
}

export type Documento = {
    id: number;
    nome: string;
    arquivo: FileField;
    status: 'pendente' | 'processado' | 'processado';
}