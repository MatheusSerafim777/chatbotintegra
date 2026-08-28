from django.core.management.base import BaseCommand, CommandError

from chat.graph import CHAT_GRAPH


class Command(BaseCommand):
    help = 'Imprime a topologia do grafo do chatbot.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--formato',
            choices=('mermaid', 'png', 'ascii'),
            default='mermaid',
            help='Formato da saída (mermaid é o padrão).',
        )
        parser.add_argument(
            '--saida',
            default='graph.png',
            help='Caminho do arquivo quando o formato for png.',
        )

    def handle(self, *args, **options):
        graph = CHAT_GRAPH.get_graph()

        if options['formato'] == 'mermaid':
            self.stdout.write(graph.draw_mermaid())
            return

        if options['formato'] == 'png':
            try:
                graph.draw_mermaid_png(output_file_path=options['saida'])
            except Exception as exc:
                raise CommandError(
                    'Não foi possível renderizar o PNG via Mermaid. '
                    'Verifique o acesso à internet ou use --formato mermaid.'
                ) from exc
            self.stdout.write(
                self.style.SUCCESS(
                    f"Imagem do grafo salva em: {options['saida']}"
                )
            )
            return

        try:
            self.stdout.write(graph.draw_ascii())
        except ImportError as exc:
            raise CommandError(
                'O formato ASCII requer o pacote grandalf. '
                'Use --formato mermaid ou instale grandalf.'
            ) from exc
