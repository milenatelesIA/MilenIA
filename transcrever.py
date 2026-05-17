#!/usr/bin/env python3
"""
Transcreve vídeos do YouTube usando yt-dlp + faster-whisper (offline).

Uso:
    python transcrever.py <URL>
    python transcrever.py --lista videos.txt
    python transcrever.py <URL> --modelo small --idioma pt --saida transcricoes/
"""

import argparse
import re
import sys
import tempfile
from pathlib import Path

import yt_dlp
from faster_whisper import WhisperModel


def sanitizar_nome(nome: str) -> str:
    nome = re.sub(r"[^\w\s-]", "", nome).strip()
    nome = re.sub(r"\s+", "_", nome)
    return nome[:120] or "video"


def baixar_audio(url: str, destino: Path) -> tuple[Path, str]:
    opts = {
        "format": "bestaudio/best",
        "outtmpl": str(destino / "%(id)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
        "no_warnings": True,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
    audio = destino / f"{info['id']}.mp3"
    titulo = info.get("title") or info["id"]
    return audio, titulo


def transcrever_arquivo(modelo: WhisperModel, audio: Path, idioma: str | None) -> tuple[str, list]:
    segmentos, _ = modelo.transcribe(
        str(audio),
        language=idioma,
        vad_filter=True,
        beam_size=5,
    )
    segmentos = list(segmentos)
    texto = " ".join(s.text.strip() for s in segmentos)
    return texto, segmentos


def formatar_srt(segmentos) -> str:
    def fmt(t: float) -> str:
        h = int(t // 3600)
        m = int((t % 3600) // 60)
        s = int(t % 60)
        ms = int((t - int(t)) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    linhas = []
    for i, seg in enumerate(segmentos, 1):
        linhas.append(f"{i}\n{fmt(seg.start)} --> {fmt(seg.end)}\n{seg.text.strip()}\n")
    return "\n".join(linhas)


def processar_url(url: str, modelo: WhisperModel, idioma: str | None, saida: Path, srt: bool):
    print(f"\n→ {url}")
    with tempfile.TemporaryDirectory() as tmp:
        try:
            audio, titulo = baixar_audio(url, Path(tmp))
        except Exception as e:
            print(f"  ✗ erro ao baixar: {e}")
            return False

        print(f"  ✓ baixado: {titulo}")
        print(f"  → transcrevendo...")

        try:
            texto, segmentos = transcrever_arquivo(modelo, audio, idioma)
        except Exception as e:
            print(f"  ✗ erro ao transcrever: {e}")
            return False

    nome = sanitizar_nome(titulo)
    txt_path = saida / f"{nome}.txt"
    txt_path.write_text(f"{titulo}\n{url}\n\n{texto}\n", encoding="utf-8")
    print(f"  ✓ salvo: {txt_path}")

    if srt:
        srt_path = saida / f"{nome}.srt"
        srt_path.write_text(formatar_srt(segmentos), encoding="utf-8")
        print(f"  ✓ salvo: {srt_path}")

    return True


def carregar_urls(lista_path: Path) -> list[str]:
    urls = []
    for linha in lista_path.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if linha and not linha.startswith("#"):
            urls.append(linha)
    return urls


def main():
    parser = argparse.ArgumentParser(description="Transcreve vídeos do YouTube com Whisper local.")
    grupo = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument("url", nargs="?", help="URL do vídeo do YouTube")
    grupo.add_argument("--lista", type=Path, help="Arquivo .txt com uma URL por linha")

    parser.add_argument("--modelo", default="small",
                        choices=["tiny", "base", "small", "medium", "large-v3"],
                        help="Modelo Whisper (padrão: small)")
    parser.add_argument("--idioma", default="pt",
                        help="Código do idioma (pt, en, es...). Use 'auto' para detectar.")
    parser.add_argument("--saida", type=Path, default=Path("transcricoes"),
                        help="Diretório de saída (padrão: transcricoes/)")
    parser.add_argument("--srt", action="store_true", help="Também gerar arquivo .srt com timestamps")
    parser.add_argument("--device", default="cpu", choices=["cpu", "cuda", "auto"],
                        help="Dispositivo de inferência (padrão: cpu)")

    args = parser.parse_args()

    if args.lista:
        if not args.lista.exists():
            print(f"erro: arquivo não encontrado: {args.lista}", file=sys.stderr)
            sys.exit(1)
        urls = carregar_urls(args.lista)
        if not urls:
            print("erro: arquivo de lista vazio", file=sys.stderr)
            sys.exit(1)
    else:
        urls = [args.url]

    args.saida.mkdir(parents=True, exist_ok=True)
    idioma = None if args.idioma == "auto" else args.idioma

    print(f"Carregando modelo Whisper '{args.modelo}' (device={args.device})...")
    modelo = WhisperModel(args.modelo, device=args.device, compute_type="int8")

    ok = sum(processar_url(url, modelo, idioma, args.saida, args.srt) for url in urls)
    print(f"\n{ok}/{len(urls)} vídeo(s) transcrito(s) em '{args.saida}/'")


if __name__ == "__main__":
    main()
