import asyncio

from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Button, Footer, Header, Input, ProgressBar, Static

from .chunking import chunk_sequence


class GeneWeaverApp(App):
    """Terminal interface for GeneWeaver genomic processing."""

    TITLE = "GeneWeaver"
    SUB_TITLE = "GPU-Accelerated CRISPR Alignment Engine"

    CSS = """
    Screen {
        align: center middle;
    }

    #main {
        width: 80%;
        height: auto;
        border: round green;
        padding: 2;
    }

    .field-label {
        margin-top: 1;
        color: cyan;
    }

    #process-button {
        margin-top: 2;
        width: 100%;
    }

    #progress {
        margin-top: 2;
    }

    #status {
        margin-top: 1;
        height: 3;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()

        with Container(id="main"):
            yield Static("GENOMIC SEQUENCE PROCESSING", classes="field-label")
            yield Static("Enter DNA sequence:")
            yield Input(
                placeholder="Example: ATGCGTACGT",
                id="sequence",
            )

            yield Static("Chunk size:", classes="field-label")
            yield Input(
                value="1000",
                placeholder="Enter chunk size",
                id="chunk-size",
            )

            yield Button("Process Sequence", id="process-button", variant="success")

            yield Static("Processing progress:", classes="field-label")
            yield ProgressBar(total=1, show_percentage=True, id="progress")
            yield Static("0 chunks processed", id="status")

        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != "process-button":
            return

        sequence = self.query_one("#sequence", Input).value
        chunk_size_text = self.query_one("#chunk-size", Input).value

        status = self.query_one("#status", Static)
        progress = self.query_one("#progress", ProgressBar)
        button = self.query_one("#process-button", Button)

        try:
            chunk_size = int(chunk_size_text)
            chunks = chunk_sequence(sequence, chunk_size)
        except (ValueError, TypeError) as error:
            status.update(f"Input error: {error}")
            return

        button.disabled = True
        progress.update(total=len(chunks), progress=0)
        status.update(f"Processing 0 of {len(chunks)} chunks...")

        for index, chunk in enumerate(chunks, start=1):
            await asyncio.sleep(0.02)

            progress.update(progress=index)
            status.update(
                f"Processed {index} of {len(chunks)} chunks "
                f"({len(chunk)} bases in current chunk)"
            )

        status.update(
            f"Completed! {len(chunks)} chunks processed, "
            f"{len(sequence)} DNA bases."
        )
        button.disabled = False


if __name__ == "__main__":
    GeneWeaverApp().run()
