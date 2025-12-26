# Code Comparator Pro 🔍

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python](https://img.shields.io/badge/Python-3.x-yellow.svg)](https://www.python.org/)

**[English](#english) | [Português](#português)**

---

<a name="english"></a>
## 🇺🇸 English

**Code Comparator Pro** is a robust desktop tool developed in Python for source code comparison (Diff Tool), visualization, and statistical analysis. Designed to be lightweight, dependency-free, and highly functional.

> **Developed for:** Jairo Brito  
> **Version:** 2.3

### 🚀 Key Features

- **Side-by-Side Comparison:** Clear visualization with syntax highlighting for additions (green), deletions (red), and matching lines.
- **Sync Scroll:** Navigate through both files simultaneously.
- **IDE Integration:** Dedicated button to open the compared code directly in your favorite IDE (VS Code, PyCharm, etc.).
- **Theme Support:**
  - ☀️ Light (Default)
  - 🌙 Dark Mode
  - 🧛 Dracula
- **Multi-language:** Full interface in Portuguese (PT-BR) and English (EN).
- **Statistics & Charts:**
  - Inserted/Deleted line counts.
  - Native Pie Chart (Canvas) showing change distribution.
- **Reports:** Export generated `diff` to `.txt` file.
- **Persistence:** Automatically saves preferences (Theme, Language, IDE Path).

### 🛠️ Requirements

- **Python 3.x** installed.
- **Libraries:** Only Python standard libraries (no `pip install` required).
  - `tkinter`, `difflib`, `json`, `subprocess`, `tempfile`

### 📦 Installation & Usage

1. Clone this repository or download the source code.
2. Run the main script:

```bash
python code-compare.py
```

3. **How to Use:**
   - Load **Original (A)** and **Modified (B)** files using buttons or drag-and-drop.
   - Click **COMPARE**.
   - Use **Settings** menu to change themes or set your IDE path.

---

<a name="português"></a>
## 🇧🇷 Português

**Code Comparator Pro** é uma ferramenta desktop robusta desenvolvida em Python para comparação de código fonte (Diff Tool), visualização de diferenças e análise estatística. Projetada para ser leve, sem dependências pesadas e altamente funcional.

> **Desenvolvido para:**  Jairo Brito  
> **Versão:** 2.3

### 🚀 Funcionalidades Principais

- **Comparação Lado a Lado:** Visualização clara com realce de sintaxe para adições (verde), remoções (vermelho) e linhas iguais.
- **Rolagem Sincronizada (Sync Scroll):** Navegue pelos dois arquivos simultaneamente.
- **Integração com IDE:** Botão dedicado para abrir o código comparado diretamente na sua IDE favorita (VS Code, PyCharm, etc.).
- **Suporte a Temas:**
  - ☀️ Claro (Padrão)
  - 🌙 Dark Mode
  - 🧛 Dracula
- **Multi-idioma:** Interface completa em Português (PT-BR) e Inglês (EN).
- **Estatísticas e Gráficos:**
  - Contagem de linhas inseridas/removidas.
  - Gráfico de pizza nativo (Canvas) mostrando a distribuição das alterações.
- **Relatórios:** Exportação do `diff` gerado para arquivo `.txt`.
- **Persistência:** Salva automaticamente suas preferências (Tema, Idioma, Caminho da IDE).

### 🛠️ Requisitos

- **Python 3.x** instalado.
- **Bibliotecas:** Apenas bibliotecas padrão do Python (não requer `pip install`).
  - `tkinter`, `difflib`, `json`, `subprocess`, `tempfile`

### 📦 Instalação e Uso

1. Clone este repositório ou baixe o arquivo fonte.
2. Execute o script principal:

```bash
python code_diff_tool.py
```

3. **Como Usar:**
   - Carregue o arquivo **Original (A)** e o **Modificado (B)** usando os botões ou colando o texto.
   - Clique em **COMPARAR**.
   - Use o menu **Configurações** para alterar o tema ou definir o caminho da sua IDE.

---

## 📝 License / Licença

This project is licensed under the **GNU General Public License v3.0 (GPLv3)** - see the [LICENSE](LICENSE) file for details.

Este projeto está licenciado sob a **GNU General Public License v3.0 (GPLv3)** - veja o arquivo [LICENSE](LICENSE) para detalhes.