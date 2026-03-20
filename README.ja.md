# LINE スタンプメーカー — Claude Code Skill

> AIでLINEスタンプをデザインする完全パイプライン。コンセプトから申請用ファイルまで。

[English](README.md) | [繁體中文](README.zh-TW.md) | **日本語**

<p align="center">
  <img src="docs/pipeline-overview.svg" alt="パイプライン概要" width="700">
</p>

## これは何？

**[Claude Code](https://claude.ai/claude-code) Skill** です。LINEスタンプ制作の全工程をガイドする、構造化された指示とスクリプトのセットです：

1. **テーマ企画** — キャラクターコンセプト、表情リスト、セット構成
2. **キャラクターデザイン** — Style Anchor（スタイルアンカー）で視覚的一貫性を確保
3. **バッチ生成** — AI画像生成と品質管理
4. **品質レビュー** — AI生成の一般的な問題を検出する体系的チェックリスト
5. **後処理** — 背景除去、リサイズ、フォーマット変換の自動化
6. **最終検証** — フォーマット準拠確認、申請準備完了

## なぜSkillが必要？

AI画像生成は強力ですが、不安定です。ガードレールなしでは、以下の問題に繰り返し直面します：

| 問題 | 発生頻度 | 影響 |
|------|----------|------|
| 1枚の画像に2体のキャラクターが出現 | 非常に多い | 再生成が必要 |
| 16枚全てフォントが異なる | ほぼ確実 | プロらしくない仕上がり |
| キャラクターが中央に配置されない | よくある | チャットでのトリミングが悪い |
| 誤った文化的・政治的シンボルの出現 | 時々 | 論争リスク |
| キャラクターサイズの不統一 | よくある | セット全体がちぐはぐに見える |

このSkillは**実践で得た教訓**を再利用可能な指示に変換し、同じ失敗を繰り返さないようにします。

## クイックスタート

### 1. Skillのインストール

Claude Codeのskillsディレクトリにコピー：

```bash
# ディレクトリ作成
mkdir -p ~/.claude/skills/line-sticker-maker

# ファイルをコピー
cp SKILL.md ~/.claude/skills/line-sticker-maker/
cp -r scripts/ ~/.claude/skills/line-sticker-maker/scripts/
```

### 2. 依存関係のインストール

後処理スクリプトにはPillowが必要です：

```bash
pip install Pillow
```

### 3. 使い方

Claude Codeで以下のように入力：

```
16個のLINEスタンプセットをデザインして、テーマは[あなたのテーマ]
```

または

```
Design a set of 16 LINE stickers featuring [your character concept]
```

Claudeが自動的にSkillを呼び出し、完全なパイプラインをガイドします。

## プロジェクト構成

```
line-sticker-maker-skill/
├── SKILL.md                          # メインSkillファイル（Claude Codeが読み取る）
├── scripts/
│   └── process_stickers.py           # 後処理：背景除去、リサイズ、フォーマット変換
├── docs/
│   └── pipeline-overview.svg         # パイプライン図
├── examples/
│   └── sample-planning-table.md      # スタンプ企画表のサンプル
├── LICENSE
└── README.md
```

## 後処理スクリプト

`scripts/process_stickers.py` はAI生成の生画像をLINE仕様に変換します：

```bash
# 基本的な使い方
python3 scripts/process_stickers.py \
  --input-dir ./my-stickers \
  --output-dir ./line_format

# スタンプごとのパディング調整
python3 scripts/process_stickers.py \
  --input-dir ./my-stickers \
  --output-dir ./line_format \
  --padding-override "04:55,08:45"
```

### 機能：

- **白背景の除去** → 透過PNG
- **370×320pxにリサイズ**、キャラクター中央配置、セーフマージン確保
- **main.png生成**（240×240）と **tab.png生成**（96×74）
- **検証** — 全ファイルが1MB以下であることを確認

### オプション：

| フラグ | デフォルト | 説明 |
|--------|-----------|------|
| `--input-dir` | （必須） | `sticker_*.png` ファイルを含むディレクトリ |
| `--output-dir` | （必須） | LINE形式ファイルの出力先 |
| `--default-padding` | `10` | デフォルトパディング（ピクセル） |
| `--bg-threshold` | `240` | 白背景検出しきい値（0-255） |
| `--padding-override` | `""` | スタンプ別パディング（例：`"04:55,08:45"`） |
| `--main-source` | `1` | main/tab画像に使用するスタンプ番号 |

## コアコンセプト：Style Anchor（スタイルアンカー）

**Style Anchor** はすべてのスタンプで共有される固定プロンプトプレフィックスで、視覚的一貫性を維持します：

```
[アートスタイル] + [キャラクター説明] + [衣装の詳細] + [文化的マーカー] + [構図ルール] + [技術仕様]
```

例：
```
Cute chibi kawaii style LINE sticker, exactly ONE single character
centered in the image, a round-faced boy with big expressive eyes
and rosy cheeks, thick black outline, cartoon style, high contrast
colors, simple clean white background, flat illustration, no shadow
```

各スタンプは表情、ポーズ、テキストだけを変えます。それ以外はすべて同一に保ちます。

## LINE Creators Market 仕様

| 素材 | サイズ (px) | 形式 | 枚数 |
|------|------------|------|------|
| メイン画像 | 240 × 240 | PNG、透過背景 | 1枚 |
| スタンプ本体 | 370 × 320 | PNG、透過背景 | 8 / 16 / 24 / 32 / 40枚 |
| トークタブアイコン | 96 × 74 | PNG、透過背景 | 1枚 |

- すべての画像：RGBA PNG、RGBカラーモード
- 最大ファイルサイズ：画像あたり1MB
- コンテンツは端から10px以上のマージンが必要

## コントリビューション

新しいAI生成の落とし穴を発見しましたか？より良いプロンプト戦略がありますか？PRを歓迎します！

特に以下の分野での貢献をお待ちしています：
- **アニメーションスタンプ対応**（APNG形式）
- **テキストオーバーレイスクリプト**（`scripts/add_text.py`）プログラムによるテキスト追加
- **追加のStyle Anchorテンプレート** — 異なるキャラクタータイプ向け
- **他のAI画像モデル向けプロンプト戦略**

## ライセンス

MIT License — [LICENSE](LICENSE) を参照。

## クレジット

[Vista](https://www.vista.tw) が制作 — AIでLINEスタンプセットをデザインした実体験から生まれました。
