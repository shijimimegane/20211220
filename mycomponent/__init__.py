import streamlit.components.v1 as components
mycomponent = components.declare_component(
    "mycomponent",
    path="./mycomponent"
)

def st_custom_input(input):
    component_value = mycomponent(input)
    return component_value
