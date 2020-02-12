extern crate web_view;

use std::process::Command;
use std::thread;
use web_view::*;

fn main() {
    let size = (1200, 900);
    let resizable = true;
    let debug = false;
    let titlebar_transparent = true;
    let frontend_cb = |_webview: &mut _, _arg: &_, _userdata: &mut _| {};
    let userdata = ();

    let html = format!(r#"
    <html>
        <head>
        <style>{css}</style>
        </head>
        <body>
        <h1>hello world</h1>
        <script>{js}</script>
        </body>
    </html>
    "#,
    // css = r#"body { background: #1d1f21; }"#,
    css = r#""#,
    js = include_str!("../www/dist.js"));

    thread::spawn(|| {
        Command::new("cmd")
            .args(&["/C", "cd gcheck && app.exe"])
            .output()
            .expect("failed to execute process");
    });

    run(
        "",
        Content::Url(format!("http://127.0.0.1:8000")),
        Some(size),
        resizable,
        debug,
        titlebar_transparent,
        move |mut webview| {
            // webview.set_background_color(0.11, 0.12, 0.13, 1.0);
        },
        frontend_cb,
        userdata
    );
}
