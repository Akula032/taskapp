**README.md**
 * ◯16行目のcommand `cd tsakapp/api` はフォルダの名前が間違っていると思います。確認してください
 * ◯`poetry install` このcommandは、コンテナが立ち上がっていない状態でも実行できますか？
 * ◯`cd taskapp/web` このcommandはフォルダの名前自体は正しいと思いますが、移動先のフォルダは本当に**web**で合っていますか？package.jsonやnode_modulesが見当たりません
 * ◯`docker compose exec api poetry run python -m migrate_db` このコマンドで指定されているコンテナの名前は正しいですか？**api**というコンテナはないと思います
 * △また、`docker compose exec {正しいコンテナ名} poetry run python -m migrate_db`を実行した場合もうまくいきませんでした。コマンドを確認してみてください。
 * ◯README.mdについては、一度、自分の環境でテストしましょう

**Backend**
 * 不要なファイル、フォルダは削除しましょう(.Zone.identifierファイル, pycacheファイル)
 * コードを見て処理が分かるようなときは、コメントは不要です。削除しましょう
 * 使われていない変数と関数は削除しましょう */src/db.py*など
 * また、コメントアウトされているコードは使う予定がないのであれば削除しましょう
 * Example... `return new_record # 作成したレコードを返す`,`response_model=AttendanceResponse   # 返すデータの型を指定`,
`# Staffテーブルからcodeで職員を検索 staff = Staff.get_or_none(Staff.code == request.code, Staff.active)`など
 * データベースの接続情報は、.envファイルを作成してそこにまとめましょう
 * pythonのdotenvというライブラリを使うと.envファイルの読み取りができます
 * schema.pyにModelが定義されているモジュールがあります。schema.pyにはSchemaをmodel.pyにはModelを定義するように統一してください
 * URLが分かりにくいです。それぞれのURLのprefixは一意になるようにしてください。現在は、task URL: `/tasks/~` done URL: `"/tasks/{task_id}/done"` になっています。どちらもprefixが*tasks*なので、FrontendでAPIリクエストのコードを見るとどのAPIにリクエストしているのか分かりません。
 * apiの*router*変数について、APIRouter()というClassにprefixというオプションを使うと省略できる部分があります。`/tasks/{task_id}/done` ==> `/{task_id}/done` のような感じで書けます
 * これは`prefix=/tasks`とした例です。参考にしてみてください
 * response_modelで設定した型と実際に`return`する変数の型は一致させましょう
 * */src/modules/done/api.py*の`def unmark_task_as_done(task_id: int)`関数では一致していないようです
 * `/src/modules/done/api.py`では*put*リクエストで新しいデータが作成されているようです。一般的に*put*はリソースの置き換えのために用いられるリクエスト形式です。特別（更新対象データがなければ、新規作成するよう）な処理がなければ*post*メソッドに変更しましょう。
 * */src/modules/task/service.py*の`def delete_task(original: Task) -> None`関数ではNoneを戻り値として返すように定義していますが、実際には`return`がありません
 * 打刻機能とログイン機能を今後も残しておくつもりであれば、ファイルの名前は統一しましょう
 * 不要な print は削除しましょう
 * task の model に done が入っていて、done/model.py が無いので、各 module 内に 作成しましょう
 * task/service のインデントがおかしい所があります。フォーマットしましょう。フォーマット機能をいれていなければ追加しましょう


**Frontend**
 * HTMLに所々、不自然な改行とコメントがありますが特に意味がなければ、改行、コメントを削除しましょう。コードが増えていったときに可読性の低下に繋がります。
 * scriptタグ内のコードにも不要と思われるコメントがあるので削除してください
 * URLを`API_BASE_URL = 'http://localhost:8000'`このように管理しているところが見られますが、URLの共通部分は*.envファイル*、もしくは*.tsファイル*にまとめてインポートするようにしてみましょう。
 * console.error,console.logは、特別な理由がなければ、基本的に削除してください
 * 使われてない関数、変数があるので、使う予定がなければ削除しましょう。
 * タスク編集モーダルについて、タイトルをスペースのみで入力して更新ボタンを押したときに、「タスクタイトルを入力してください」のようなトーストを出すといいかもしれないです。タスク追加画面ではそのようになっていたので、動作を統一しましょう。
 * このフィールドを入力してください or トーストを出すかはどちらかにしましょう
 * タスク追加画面とタスク編集モーダルでタイトル入力フィールドをフォーカスしたときにアウトラインが強調されますが、その設定を解除してください
 * タスク追加画面とタスク編集モーダルのタイトル入力フィールドで入力が始まる位置と枠線の間隔をもう少し広げましょう
 * ヘッダーの一番左の文字が、黄色いボックスの左端と揃うようにしてください。タスクを追加ボタンも一緒に揃えましょう
 * ヘッダーの文字の部分をクリックしたらタスク管理システムのメイン画面に遷移するようにしてください
 * 完了/未着手ラベルの左端とタスクタイトルの左端を揃えましょう
 * 同じタスクを登録できてしまうので、エラーにしましょう
 * class 名を()内に書かない様統一しましょう
 * トーストのテキストは単語にするか、文章にするか統一しましょう
 * App.vue
  - pug にしましょう
  - scss が入っていないのと、scss を使える部分なので、使ってみましょう
    - app-layout  &content のつなぎ方が出来そうなので書いてみましょう
 * router
  - ルートは taskapp にしましょう(メイン画面なので)
 * Header.vue 不要な class, css 指定は削除しましょう
 * KanbanBoard.vue
  - このページのコンポーネント化は良い感じだと思います
  - 12,13 行目 task-group-list の css 使ってますか？
  - ※現段階で不要な css は書かない方が良いです（横スクロールとか、space とか。。。修正は不要）プロジェクト入ったら現段階以外の記述は不要なものと認識されるので
  - Modal と DeleteModal は トップの div のなかに入れましょう
  - 115, 117 行目 型付けよう　(task)　→　(task: { id: number })
  - トーストの文面をよりユーザー向けにしましょう
      - 変更はありませんでした→修正をしてくださいでリターン
      - 更新処理が完了しましたが、変更は確認できませんでした → なぜ更新処理をおこないました？
      - タスクの更新に失敗しました → できる限りなんのエラーか、何かが被ってるとか一致しないとか、api でエラーの種類を分けて使えるとベスト
  - 252, 267 行目 catch ？？？
  - 272 行目 goToAddTAskPage camel ケースミスってそうです**
  - .board-header, status-badge 使ってますか？
 * TaskBtn.vue
  - 2行目 my-4 で行ける記述が多い時はなるべくまとめた方が良い(記述はより少ない方が可読性が上がります)
  - .addtaskbtn と .board-header 使ってない
  - class 名書き方統一 ケバブケースが良さそうです
 * DeleteModal.vue
  - 3, 5, 7,13行目 modal-○○ 使ってますか？
  - 11行目 mt, mb まとめましょう
  - 15行目 cancel-btn 使ってますか？
  - 20行目 confirm-delete-btn 使ってますか？
  - 15, 20 の button px で大きさ指定してるけど文字列の長さによって双方にずれが出る可能性があるので、width で指定しましょう
  - 18, 23行目 focus ○○ 使ってますか？
 * Modal.vue
  - フォルダのネーミング変えた方が良いです（Modal 色んな種類あるから何をする為の Modal なのか分かりやすく）
  - 3, 7, 46行目 modal-○○を使ってますか？
  - 8行目 text-xl 記述ミスしてます
  - 9行目 close-btn, focus-outline-none 使ってますか？
  - × の削除ボタン汎用的に使えるから余力があれば component 化 (モーダル増えるから)しましょう
  - form component 化出来た方が良いです
  - 16 行目 edit-task-title 何で使ってますか ID ?
      - appearance-none 使ってますか？
  - 26, 27 行目、「タスクを追加」で津川君が 〇(ラジオ) と 未着手 のズレが気になって直したからここもついでに直しましょう
      - cursor-pointer 追記した方が良い（〇(ラジオ) の部分でポインターになってない）
  - 47行目 cancel-btn 使ってますか？
  - 51行目 submit-btn 使ってますか？
  - 47, 51 の button px でボタンの大きさ指定すると文字列によって双方にずれが出るから width で指定しましょう
 * TaskGroup.vue
  - task-group-list-wrapper は使ってますか？
 * TaskCard.vue
  - 3行目 mr, ml まとめましょう
  - 5行目 status-badge-container 使ってますか？
  - 8, 12行目 .font-semibold.text-white 親に指定した方が良い(記述が一つで済むので、項目が増えるとその分同じ記述が増えちゃいます)
  - 14行目 task-header 使ってますか？
    - mt, mb まとめましょう
  - 16行目 h3 ？？？
  - 18, 21行目 edit-btn, delete-btn 使ってますか？
    - button px でボタンの大きさ指定すると文字列によって双方にずれが出るから width で指定しましょう
  - 100行目 uncomplete-btn 使ってますか？
  - バッジ と テキストの始まり位置あわせましょう
 * AddTask.vue
  - 9, 21, 29 行目 label テキスト入れてないけど何のためにありますか？
  - form も components 化できたらよいです
  - cursor-pointer 追記しましょう（〇(ラジオ) の部分でポインターになってない）
  - radio ボタン for で回せたらさらに良い（進行中の項目とか多い場合、同じ記述並ぶ）
  - catch で登録できなかった理由を表示できたらなお良いです
  - ボタンの border を削除しましょう(他の画面のボタンと統一)
  - 余力があれば、ボタンエリアも汎用的にコンポーネント化出来たら良いです
  


**Git**
 * こまめなcommitとbranchの作成をあまりしていなかったと思うので、次の課題からは意識しましょう

**Overall**
　* アプリの機能は特に大きなバグはなく、よくできていると思います。
　* コードは、改行、コメント、使用されていない関数、変数がありましたが、ロジックは特に問題ありませんでした。
　* 命名規則やDRY原則など、コーディングの基本的なルールが守られていて良いと思います。
　* 軽微な修正点が少しありますが、致命的なものはないので全体的には良い仕上がりに感じました。
　* 不要な物が沢山ありそうなので使うときに確認しながら、必要なものだけを記述出来ると良いですね。(可読性が上がります)