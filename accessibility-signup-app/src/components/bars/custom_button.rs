use yew::prelude::*;
use stylist::{yew::styled_component};

#[derive(Properties, PartialEq)]
pub struct Props {
    pub label: String
}

#[styled_component(CustomButton)]
pub fn custom_button(props: &Props) -> Html {
    html! {
        <button class="text-2xl ">
            {&props.label}
        </button>
    }
}
