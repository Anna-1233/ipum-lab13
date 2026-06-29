import base64
import io
import matplotlib.pyplot as plt
from typing import Annotated
from fastmcp import FastMCP


mcp = FastMCP("Visualization Server")


@mcp.tool(description="Creates a line plot from given data and returns it as a base64 encoded image.")
def line_plot(
        data: Annotated[list[list[float]], "One or more lists of numbers to plot. Each list is a separate line."],
        names: Annotated[list[str], "Names for each data series"] = "",
        title: Annotated[str, "Optional title of the plot"] = "",
        x_label: Annotated[str, "Optional label for the X axis"] = "",
        y_label: Annotated[str, "Optional label for the Y axis"] = "",
        legend: Annotated[bool, "Whether to show the legend (default True if multiple lines, else False)"] = False
) -> str:

    plt.figure()

    for i, line_data in enumerate(data):
        label = names[i] if i < len(names) else f"Series {i + 1}"
        plt.plot(line_data, label=label)

    if title:
        plt.title(title)
    if x_label:
        plt.xlabel(x_label)
    if y_label:
        plt.ylabel(y_label)
    if legend or len(data) > 1:
        plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close()

    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode("utf-8")

    return image_base64


if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8003)