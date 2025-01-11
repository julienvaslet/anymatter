import qrcode
import io
import logging
from math import floor

logger = logging.getLogger(__name__)


def print_qr_code(data, description=None, padding=8):
    """Create the QRCode, print it with # 2x bigger to make it readable with Apple Home."""

    stream = io.StringIO()

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=0,
    )

    qr.add_data(data)
    qr.print_ascii(out=stream)

    upper, lower, full = [bytes((code,)).decode("cp437") for code in (223, 220, 219)]
    qr_data = [[],[]]
    line_index = 1

    for char in stream.getvalue():
        if char == "\n":
            line_index += 2
            qr_data.extend([[],[]])
            continue

        qr_data[line_index - 1].extend(2 * ["#" if char in [full, upper] else " "])
        qr_data[line_index].extend(2 * ["#" if char in [full, lower] else " "])
    
    stream.close()

    qr_data = [" " * padding + "".join(line) + " " * padding for line in qr_data]
    qr_width = len(qr_data[0])
    qr_text = "\n" * floor(padding / 2) + "\n".join(qr_data).rstrip() + "\n" * floor(padding / 2)
    
    output = [qr_text]

    if description:
        for line in description.split("\n"):
            line_length = len(line)

            if (line_length < qr_width):
                left_padding = " " * (floor((qr_width - line_length) / 2))
                line = f"{left_padding}{line}"

            output.append(line)
        
        output.append("\n")
    
    logger.info("\n".join(output))