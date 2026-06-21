import os
import hashlib
import json

# Pasta onde estão os arquivos atualizados (a pasta "files" do repositório)
PASTA_FILES = "files"
SAIDA = "manifest.json"

def calcular_hash(caminho_arquivo):
    sha256 = hashlib.sha256()
    with open(caminho_arquivo, "rb") as f:
        for bloco in iter(lambda: f.read(8192), b""):
            sha256.update(bloco)
    return sha256.hexdigest()

def gerar_manifest():
    arquivos = []
    IGNORAR = {"desktop.ini", "thumbs.db", ".ds_store"}

    for raiz, _, nomes in os.walk(PASTA_FILES):
        for nome in nomes:
            if nome.lower() in IGNORAR:
                continue

            caminho_completo = os.path.join(raiz, nome)
            caminho_relativo = os.path.relpath(caminho_completo, PASTA_FILES).replace("\\", "/")
            tamanho = os.path.getsize(caminho_completo)
            hash_arquivo = calcular_hash(caminho_completo)
            arquivos.append({
                "path": caminho_relativo,
                "hash": hash_arquivo,
                "size": tamanho
            })
            print(f"OK: {caminho_relativo}")

    manifest = {"files": arquivos}
    with open(SAIDA, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"\nmanifest.json gerado com {len(arquivos)} arquivo(s).")

if __name__ == "__main__":
    gerar_manifest()