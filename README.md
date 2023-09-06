# reading-time
Calculate reading time for articles from their URLs

## How to Use
1. Checkout this repository.
2. Set up a python virtual environment with:

    ```
    python -m venv --prompt pdf-password .venv
    ```

3. Source the virtual environment with:

    ```
    source .venv/bin/activate
    ```

4. Install required packages using `pip`:

    ```
    pip install pip-tools
    pip-compile requirements.in
    pip-sync
    ```

5. Run the script with:

    ```
    python reading_time.py <url>
    ```

## Options

The command line options available to the script are shown below.

| Option | Description |
| ------ | ------ |
| `-h`, `--help` | Show the help message. |
| `-s <wpm>`, `--reading-speed <wpm>` | Set the reading speed in in words per minute. The default value is 200. |
| `-a`, `--alternate` | Use [`readabilipy`](https://github.com/alan-turing-institute/ReadabiliPy) instead of [`readability`](https://github.com/buriy/python-readability) to extract the article text. |
| `-w`, `--whole-page` | Use the whole page when calculating reading speed instead of just the main article text. |
