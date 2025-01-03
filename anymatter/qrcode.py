import qrcode
import io
import sys

def print_qr_code(data, out=sys.stdout):
    """Create the QRCode, print it with # 2x bigger to make it readable with Apple Home."""

    stream = io.StringIO()

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
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

    for line in qr_data:
        print("".join(line), file=out)