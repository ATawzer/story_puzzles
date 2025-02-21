import streamlit as st
from project_muse.db import init_db
from project_muse.template.scene import SceneTemplate, SceneTemplateTag
from project_muse.scene import Scene
from project_muse.entity.template import (
    CharacterTemplate, 
    ObjectPropTemplate, 
    LandmarkTemplate,
    CreatureTemplate,
    EntityType,
    BaseEntityTemplate
)
from project_muse.ui.types import SelectionState
from project_muse.ui.callbacks import on_entity_change, on_template_change

def init_app():
    """Initialize the database connection"""
    init_db()

    # Initialize session state for persistent objects
    if 'scene' not in st.session_state:
        st.session_state.scene = Scene(None)
    if 'template' not in st.session_state:
        st.session_state.template = None
    if 'selection_state' not in st.session_state:
        st.session_state.selection_state = SelectionState({}, {}, None)

def get_entity_options(entity_type: EntityType):
    """Get all entities of a specific type from the database"""
    if entity_type == EntityType.CHARACTER:
        return CharacterTemplate.objects.all()
    elif entity_type == EntityType.OBJECT_PROP:
        return ObjectPropTemplate.objects.all()
    elif entity_type == EntityType.LANDMARK:
        return LandmarkTemplate.objects.all()
    elif entity_type == EntityType.CREATURE:
        return CreatureTemplate.objects.all()
    return []

def scene_template_selector():
    """Render the scene template selector"""
    templates = SceneTemplate.objects.all()
    template_names = [t.name for t in templates]
    selected_template_name = st.selectbox(
        "Choose a scene template:",
        options=template_names,
        key="template_selector",
        on_change=on_template_change
    )
    st.session_state.template = SceneTemplate.objects(name=selected_template_name).first()

def scene_preview():
    """Render the scene preview"""
    scene_template = st.session_state.template
    scene = Scene(scene_template)
    st.session_state.scene = scene
 
    st.write("Scene Preview")
    st.markdown(f"**{scene.get_filled_description()}**")

def render_left_panel():
    """Render the left panel containing the scene template and preview"""
    with st.container():
        st.subheader("Scene Template")
        scene_template_selector()
        scene_preview()

def entity_selector(tag: SceneTemplateTag):
    """Render a single entity selector for a given tag"""
    # Get available entities
    all_entities = get_entity_options(tag.entity_type)
    selection_state: SelectionState = st.session_state.selection_state
    
    # Filter out used entities
    used_entities = selection_state.used_entities.get(tag.entity_type.value, set())
    available_entities = [e for e in all_entities if e.name not in used_entities or 
                       tag.tag_name in selection_state.selections and 
                       selection_state.selections[tag.tag_name][1].name == e.name]
    
    # Create options dictionary
    entity_options = {str(entity): entity for entity in available_entities}
    
    if entity_options:
        # Get currently selected entity for this tag if it exists
        current_selection = None
        if tag.tag_name in selection_state.selections:
            current_selection = str(selection_state.selections[tag.tag_name][1])
        
        st.selectbox(
            f"Choose {tag.entity_type.value} for '{tag.tag_name}':",
            options=list(entity_options.keys()),
            key=f"select_{tag.tag_name}",
            index=list(entity_options.keys()).index(current_selection) if current_selection else 0,
            on_change=lambda: on_entity_change(tag, entity_options[st.session_state[f"select_{tag.tag_name}"]])
        )
    else:
        st.error(f"No available {tag.entity_type.value} entities for '{tag.tag_name}'")

def sentence_selector(sentence_num: int, tags: list[SceneTemplateTag]):
    """Render entity selectors for a single sentence"""
    st.markdown(f"**Sentence {sentence_num}**")
    for tag in tags:
        entity_selector(tag)

def render_right_panel(template: SceneTemplate, scene: Scene):
    """Render the right panel containing entity selectors"""
    if not template:
        return None
    
    st.subheader("Choose Entities")
    
    # Initialize selection state if not exists
    if 'selection_state' not in st.session_state:
        st.session_state.selection_state = SelectionState({}, {}, scene)
    
    # Group tags by sentence
    tags_by_sentence = template.get_tags_by_sentence()
    
    # Process each sentence
    for sentence_num, tags in sorted(tags_by_sentence.items()):
        sentence_selector(sentence_num, tags)

    if st.button("Reset Selections"):
        st.session_state.selection_state.clear()
        st.rerun()

def main():
    """Main function to run the app"""
    init_app()

    # Layout
    st.set_page_config(layout="wide")
    st.title("Story Scene Creator")
    left_col, right_col = st.columns([1, 3])

    # Left panel (Scene Template)
    with left_col:
        render_left_panel()

    # Right panel (Entity Selection)
    with right_col:
        render_right_panel(st.session_state.template, st.session_state.scene)

if __name__ == "__main__":
    main() 