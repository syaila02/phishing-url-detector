
"""
Modul Validasi URL
Tugas: Anggota 2 (Backend)
Deskripsi:
    Memvalidasi format URL sebelum diteruskan ke model
    Machine Learning untuk proses deteksi phishing.
"""

import ipaddress
import re
import unicodedata
from urllib.parse import urlsplit


MAX_URL_LENGTH = 2048


class URLValidationError(ValueError):
    """Exception khusus untuk kesalahan validasi URL."""
    pass


def validate_url(url: str) -> str:
    """
    Memvalidasi URL dari input pengguna.

    Parameter:
        url (str): URL yang akan diperiksa.

    Mengembalikan:
        str: URL yang sudah dibersihkan dari spasi di awal/akhir.

    Raises:
        URLValidationError: Jika URL tidak memenuhi ketentuan.
    """

    # 1. Periksa tipe data
    if not isinstance(url, str):
        raise URLValidationError("Input URL harus berupa teks.")

    # 2. Tolak karakter kontrol
    if any(unicodedata.category(char) == "Cc" for char in url):
        raise URLValidationError(
            "URL mengandung karakter kontrol yang tidak diperbolehkan."
        )

    # 3. Bersihkan spasi di awal dan akhir
    clean_url = url.strip()

    if not clean_url:
        raise URLValidationError("URL tidak boleh kosong.")

    # 4. Periksa panjang URL
    if len(clean_url) > MAX_URL_LENGTH:
        raise URLValidationError(
            f"Panjang URL melebihi batas {MAX_URL_LENGTH} karakter."
        )

    # 5. Tolak spasi di tengah URL
    if any(char.isspace() for char in clean_url):
        raise URLValidationError(
            "URL tidak boleh mengandung spasi. Gunakan URL encoding jika diperlukan."
        )

    # 6. Periksa skema URL
    scheme_match = re.match(
        r"^([a-zA-Z][a-zA-Z0-9+.-]*)://",
        clean_url
    )

    if scheme_match:
        scheme = scheme_match.group(1).lower()

        if scheme not in ("http", "https"):
            raise URLValidationError(
                "Skema URL hanya boleh menggunakan HTTP atau HTTPS."
            )

        parse_target = clean_url

    else:
        # Tolak penulisan HTTP/HTTPS yang tidak lengkap
        if re.match(r"^https?:", clean_url, re.IGNORECASE):
            raise URLValidationError(
                "Format skema URL tidak lengkap. Gunakan http:// atau https://."
            )

        # URL tanpa skema tetap diperbolehkan
        parse_target = "http://" + clean_url

    # 7. Parsing URL
    try:
        parsed = urlsplit(parse_target)
        hostname = parsed.hostname
        port = parsed.port

    except ValueError:
        raise URLValidationError(
            "Format URL, alamat IP, atau nomor port tidak valid."
        )

    # 8. Pastikan hostname tersedia
    if not parsed.netloc or not hostname:
        raise URLValidationError(
            "URL harus memiliki nama domain atau alamat IP."
        )

    # 9. Periksa nomor port
    if port is not None and not (1 <= port <= 65535):
        raise URLValidationError(
            "Nomor port harus berada antara 1 sampai 65535."
        )

    # 10. Validasi hostname sebagai alamat IP
    try:
        ip_address = ipaddress.ip_address(hostname)

        if isinstance(ip_address, ipaddress.IPv6Address):
            raise URLValidationError(
                "Alamat IPv6 belum didukung oleh ekstraksi fitur model."
            )

    except ValueError as error:
        # Pertahankan error khusus untuk IPv6
        if isinstance(error, URLValidationError):
            raise

        # Jika bukan IP, periksa sebagai nama domain
        # Tolak hostname numerik yang bukan IPv4 valid
        if re.fullmatch(r"[0-9.]+", hostname):
            raise URLValidationError(
                "Format alamat IPv4 tidak valid."
            )

        try:
            ascii_hostname = hostname.rstrip(".").encode(
                "idna"
            ).decode("ascii").lower()
        except UnicodeError:
            raise URLValidationError(
                "Nama domain tidak valid."
            )

        if not ascii_hostname or len(ascii_hostname) > 253:
            raise URLValidationError("Panjang nama domain tidak valid.")

        labels = ascii_hostname.split(".")
        # Domain harus memiliki minimal dua bagian,
        # misalnya example.com atau google.co.id.
        if len(labels) < 2:
            raise URLValidationError(
                "Nama domain tidak valid. Masukkan domain lengkap, misalnya example.com."
            )


        for label in labels:
            if (
                not label
                or len(label) > 63
                or not re.fullmatch(
                    r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?",
                    label
                )
            ):
                raise URLValidationError(
                    "Format nama domain tidak valid."
                )

    return clean_url
