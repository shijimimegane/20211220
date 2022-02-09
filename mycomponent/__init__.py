import streamlit.components.v1 as components
mycomponent = components.declare_component(
    "mycomponent",
    path="./mycomponent"
)

def st_custom_input():
    component_value = mycomponent()
    return component_value
