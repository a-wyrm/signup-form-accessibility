use yew::prelude::*;
use stylist::{yew::styled_component, style};

#[derive(Properties, PartialEq)]
pub struct Props {
    pub title: String,
    pub color: Color,
    pub on_load: Callback<String>
}

#[derive(PartialEq)]
pub enum Color {
    Normal, 
    Ok,
    Error
}

impl Color{
    pub fn to_string(&self) -> String {
        match self{
            Color::Normal => "normal".to_owned(),
            Color::Ok => "ok".to_owned(),
            Color::Error => "error".to_owned(),
        }
    }
}

#[styled_component(MainTitle)]
pub fn main_title(props: &Props) -> Html {

    props.on_load.emit("Loaded.".to_owned());

    let stylesheet = style! {
        r#"
        .normal{
            color: black;
        }
        .ok{
            color: orange;
        }
        .error {
            color: red;
        }
        "#
    }.unwrap();

    html! {
        <h1 class={&props.color.to_string()}>{&props.title}</h1>
    }
}