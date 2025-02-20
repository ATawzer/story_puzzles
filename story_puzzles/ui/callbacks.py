import streamlit as st
from .types import SelectionState
from ..scene import Scene
from ..scene.template import SceneTemplate, SceneTemplateTag
from ..entity.template.base import BaseEntityTemplate

def on_entity_change(tag: SceneTemplateTag, new_entity: BaseEntityTemplate):
    """Handle entity selection changes"""
    selection_state: SelectionState = st.session_state.selection_state
    scene: Scene = st.session_state.scene
    
    # Remove any downstream selections that used the previously selected entity
    if tag.tag_name in selection_state.selections:
        old_tag, old_entity = selection_state.selections[tag.tag_name]
        
        # Find all downstream tags (higher sentence numbers)
        downstream_tags = []
        for other_tag_name, (other_tag, other_entity) in selection_state.selections.items():
            if (other_tag.sentence_num > tag.sentence_num and 
                other_entity.name == old_entity.name):
                downstream_tags.append(other_tag_name)
        
        # Remove downstream selections
        for tag_name in downstream_tags:
            selection_state.remove_selection(tag_name)
    
    # Add new selection
    selection_state.add_selection(tag, new_entity)
    
    # Update scene
    scene.create_entity_by_tag(tag, new_entity)

def on_template_change():
    """Handle template selection changes"""
    template: SceneTemplate = st.session_state.template
    
    # Create new scene and selection state
    st.session_state.scene = Scene(template)
    st.session_state.selection_state = SelectionState({}, {}, st.session_state.scene) 