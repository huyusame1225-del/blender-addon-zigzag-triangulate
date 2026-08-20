# Zigzag Triangulate

Blender extension that triangulates selected connected quad faces with alternating diagonal directions, producing a zigzag pattern.

選択した隣接四角面を、交互の対角線でジグザグに三角形化するBlenderエクステンションです。

## ⬇️ Blender 5.2対応版をダウンロード

[![Zigzag Triangulate v1.0.1をダウンロード](https://img.shields.io/badge/Blender%205.2対応版をダウンロード-v1.0.1-E87D0D?style=for-the-badge&logo=blender&logoColor=white)](https://github.com/huyusame1225-del/blender-addon-zigzag-triangulate/releases/download/v1.0.1/zigzag_triangulate-1.0.1-blender-5.2.zip)

### [ボタンが表示されない場合はこちらをクリック](https://github.com/huyusame1225-del/blender-addon-zigzag-triangulate/releases/download/v1.0.1/zigzag_triangulate-1.0.1-blender-5.2.zip)

> **初めて使う方へ:** 「Source code」ではなく、上のオレンジ色のボタンから
> `zigzag_triangulate-1.0.1-blender-5.2.zip` をダウンロードしてください。

## Features / 機能

- Alternates the diagonal direction across connected selected quads
- Handles multiple disconnected selection islands
- Leaves triangles and n-gons unchanged
- Offers a **Reverse Pattern** option
- Supports Blender's Undo system
- Available from the face context menu and F3 operator search

## Requirements / 対応環境

- Blender 5.2 or later / Blender 5.2以降

## Installation / インストール

1. Download `zigzag_triangulate-1.0.1-blender-5.2.zip` from [Releases](../../releases).
2. In Blender, open **Edit → Preferences → Extensions**.
3. Open the menu in the upper-right corner and choose **Install from Disk**.
4. Select the downloaded ZIP file.

## Usage / 使い方

1. Enter Edit Mode on a mesh and switch to Face Select.
2. Select one or more connected quad faces.
3. Right-click and choose **Zigzag Triangulate**.

You can also search for **Zigzag Triangulate** with F3. Use **Reverse Pattern** in the Adjust Last Operation panel to flip the pattern.

メッシュの編集モードで四角面を選択し、右クリックから **Zigzag Triangulate** を実行します。F3検索からも実行できます。「最後の操作」パネルの **Reverse Pattern** で向きを反転できます。

## License

GPL-3.0-or-later

