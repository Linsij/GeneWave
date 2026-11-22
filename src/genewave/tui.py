
import asyncio

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Button, Footer, Header, Input, ProgressBar, Static

from .alignment import smith_waterman
from .chunking import chunk_sequence


class GeneWeaverApp(App):
    """Terminal interface for GeneWeaver genomic alignment."""

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

    #results {
        margin-top: 1;
        height: auto;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()

        with Container(id="main"):
            yield Static("GENOMIC SEQUENCE ALIGNMENT", classes="field-label")

            yield Static("Enter DNA sequence:")
            yield Input(
                placeholder="Example: ATGCGTACGT",
                id="sequence",
            )

            yield Static("Enter reference DNA sequence:", classes="field-label")
            yield Input(
                placeholder="Example: ATGCGTACGT",
                id="reference",
            )

            yield Static("Chunk size:", classes="field-label")
            yield Input(
                value="1000",
                placeholder="Enter chunk size",
                id="chunk-size",
            )

            yield Button(
                "Align DNA Sequence",
                id="process-button",
                variant="success",
            )

            yield Static("Alignment progress:", classes="field-label")
            yield ProgressBar(total=1, show_percentage=True, id="progress")
            yield Static("0 chunks processed", id="status")
            yield Static("Alignment results will appear here.", id="results")

        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != "process-button":
            return

        sequence = self.query_one("#sequence", Input).value
        reference = self.query_one("#reference", Input).value
        chunk_size_text = self.query_one("#chunk-size", Input).value

        status = self.query_one("#status", Static)
        progress = self.query_one("#progress", ProgressBar)
        button = self.query_one("#process-button", Button)
        results_widget = self.query_one("#results", Static)

        try:
            chunk_size = int(chunk_size_text)
            chunks = chunk_sequence(sequence, chunk_size)
        except (ValueError, TypeError) as error:
            status.update(f"Input error: {error}")
            return

        button.disabled = True
        results_widget.update("Starting Smith-Waterman alignment...")
        progress.update(total=len(chunks), progress=0)
        status.update(f"Aligning 0 of {len(chunks)} chunks...")

        alignment_results = []

        try:
            for index, chunk in enumerate(chunks, start=1):
                result = smith_waterman(chunk, reference)

                alignment_results.append(
                    f"Chunk {index}: Score = {result.score}\n"
                    f"Sequence positions: {result.start1}-{result.end1}\n"
                    f"Reference positions: {result.start2}-{result.end2}\n"
                    f"Aligned sequence: {result.aligned_sequence1[:60]}\n"
                    f"Reference match: {result.aligned_sequence2[:60]}"
                )

                progress.update(progress=index)
                status.update(
                    f"Aligned {index} of {len(chunks)} chunks "
                    f"({len(chunk)} bases)"
                )

                await asyncio.sleep(0)

            results_widget.update("\n\n".join(alignment_results))

            status.update(
                f"Completed! {len(chunks)} chunks aligned, "
                f"{len(sequence)} DNA bases processed."
            )

        except (ValueError, TypeError) as error:
            status.update(f"Alignment error: {error}")

        finally:
            button.disabled = False


if __name__ == "__main__":
    GeneWeaverApp().run()
