use serde::{Deserialize, Serialize};
use yew::prelude::*;
use stylist::{yew::styled_component, Style};
use gloo::console::log;


// modular components
mod components;
use components::bars::main_title::{Color, MainTitle};
use components::bars::custom_button::CustomButton;

const STYLE_FILE: &str = include_str!("styles/main.css");

#[derive(Serialize, Deserialize)]
struct Burger {
    id: usize,
    type_of_burg: String,
    tastiness: String,
    ingredients: u8
}


#[function_component(Comp)]
fn comp() -> Html {

    let burger_list = vec![
        Burger {
            id: 1,
            type_of_burg: "Fried Green Tomato Burger".to_string(),
            tastiness: "Yummy".to_string(),
            ingredients: 5
        },
        Burger {
            id: 2,
            type_of_burg: "PATRICK BURGER".to_string(),
            tastiness: "BIG BURGER".to_string(),
            ingredients: 1
        }
    ];

    let singular_burger = Burger {
        id: 1,
        type_of_burg: "Fried Green Tomato Burger".to_string(),
        tastiness: "Yummy".to_string(),
        ingredients: 5
    };

    let burgers = burger_list.iter().map(|burg| html! {
        <p key={burg.id}>{format!("{}: {} -- {} ingredients", burg.type_of_burg, burg.tastiness, burg.ingredients)}</p>
    }).collect::<Html>();

    log!("text", serde_json::to_string_pretty(&singular_burger).unwrap());
    html! {
        <div class="burger">{burgers}</div>
    }
}

#[styled_component(StyledDiv)]
pub fn styled_div() -> Html {

    let opt = Some(true);
    let main_title_load = Callback::from(|message: String| log!(message));

    html! {
        <div>
            <MainTitle title="Authability" color={Color::Normal} on_load={main_title_load}/>
            <div class="burgerList">
                <h3>{"These burgs you gotta eat..."}</h3>
            </div>
            <Comp />
            if let Some(opt) = Some(true) {
                <p>{opt}</p>
            }
        </div>
    }
}

#[function_component(App)]
pub fn app() -> Html {
    let stylesheet = Style::new(STYLE_FILE).unwrap();
    html! {
        <div class={stylesheet}>
            <StyledDiv />
            <div class="absolute">{"Row 2"}</div>
            <CustomButton label="Here"/>
        </div>
    }
}
