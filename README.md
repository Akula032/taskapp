＃タスク管理システム


プロジェクトのディレクトリは2つです。
それぞれに依存関係や環境を構築します。
~/taskapp/api -バックエンド
~/taskapp/web -フロントエンド

※１，２のコマンドはUbuntuターミナルで実行してください

1.リポジトリのクローン
    プロジェクトディレクトリで以下のコマンドにてgitリポジトリをクローンします。
	

    - git clone git@bitbucket.org:paradigm_shift/taskapp.git
	
    ※現時点で最新のブランチである release/develop に移動します
    以下のコマンドを実行してください

    - cd taskapp
    - git checkout release/develop



2.Dockerコンテナのビルド及び起動
    以下のコマンドでコンテナのビルドと起動を行ってください。

    - docker compose build
    - docker compose up

3.環境の構築
    ※ここからはDockerコンテナが起動している前提で進みます。

    Ubuntuターミナルで新しくタブを開きます。
    ~/taskapp に移動して以下のコマンドを実行し、VSCodeを開きます。

        - code .

    実行した際に開かれるウィンドウはローカル環境のものなので、
    VSCode左側サイドパネルのリモートエクスプローラーから開発コンテナ内の
    demo-appとwebをそれぞれ新しいウィンドウで開きます。

    api環境の構築
        VSCodeで開いたdemo-app内のターミナルで以下のコマンドを実行しpyproject.tomlを作成します。

        - poetry install 

    web環境の構築
        VSCodeで開いたweb内のターミナルで以下のコマンドでライブラリやツールをインストールします。

         - npm install



4.データベースのマイグレーション
    apiプロジェクト内の migrate_db に基づいてデータベースを構築します。
    Ubuntuターミナルで以下のコマンドでDBのマイグレーションを行ってください。

    - docker compose exec demo-app poetry run python -m migrate_db

    正常にマイグレーションが完了すれば

    「テーブルのデータを削除しました」
    「新しくテーブルを作成しました」

    という案内が表示されます。


5.タスク管理システムの動作確認
    ブラウザにて以下のURLを入力してください。　※開発環境ではChromeを使用しています

    api: http://localhost:8000/docs
    web: http://localhost:5173/