import streamlit as st
from typing import Generator, Optional, Dict, Union, List
# from groq import Groq # Keep if you plan to integrate later
import random
import time

# --- Constants ---
STATE_SUPERPOSITION = "Superposition ✨"
STATE_ENTANGLEMENT = "Entanglement 🔗"
STATE_MEASURED = "Measured / Collapsed 💥" # Combined concept for simplicity
NO_STATE = "Qubits Initialized (|0⟩ state)"

# --- Enhanced Explanations with Variations ---
def get_ai_explanation(state_key: str) -> str:
    """
    Simulate AI-generated, more engaging explanations for quantum states,
    with variations for fun. Bo the AI Dog reporting! 🐾
    """
    explanations = {
        "superposition": [
            "Woof! Superposition is like my favorite chew toy AND a tennis ball AT THE SAME TIME! 🎾🦴 Your qubit isn't just |0⟩ or |1⟩, it's a mix! This lets quantum computers explore possibilities like sniffing out *all* the treats at once! 🤯",
            "Imagine a coin spinning perfectly on its edge 🪙! That's superposition! Your qubit is both heads (|0⟩) **and** tails (|1⟩) simultaneously... until we peek! 👀 It's this quantum fuzziness that gives QC its power!",
            "Think quantum hide-and-seek! 🫣 The qubit is hiding in |0⟩ and |1⟩ states at the same time! Superposition means possibilities galore until the measurement 'finds' it!"
        ],
        "entanglement": [
            "Bark bark! Entanglement! 🧠✨ Two qubits become best buds, linked FOREVER, no matter how far apart! Measure one, and you instantly know the state of the other. It's like knowing if my tail is wagging just by looking at my twin miles away! 🤯 Einstein called it 'spooky' 👻, I call it awesome!",
            "Entanglement is the ultimate quantum connection! 🤝 Imagine two magic coins 🪙🔗🪙. If one lands heads, the other *instantly* lands tails (or heads, depending on setup), even across the universe! This deep link is vital for quantum communication and teleportation!",
            "Get ready for mind-bending links! Entangled qubits share the same destiny. Like two synchronized dancers 👯‍♀️, their moves are perfectly correlated, creating a powerful shared quantum state!"
        ],
        "measured": [
            "Aha! The moment of truth! 🥁 Measuring a superposition or entangled state forces it to PICK ONE! 💥 Like that spinning coin finally landing - heads (|0⟩) or tails (|1⟩). No more quantum fuzziness, just a clear answer! This is how we get results!",
            "POP! Goes the quantum state! ✨➡️🌳 Measurement collapses the wave function. The qubit ditches its 'maybe' state and becomes definite - either |0⟩ or |1⟩. It's like flipping a quantum switch from 'blurry' to 'sharp'!",
            "Observation time! 🧐 Peeking at a qubit in superposition makes it choose! It snaps out of its multi-state dream into a concrete |0⟩ or |1⟩ reality. The quantum magic settles into a classical outcome!"
        ],
         "initialized": [
            "Okay, team! We've got our qubits lined up, fresh and ready! 🐶 They're all starting in the reliable |0⟩ state. Think of it as the 'off' switch before we unleash the quantum weirdness!",
            "Fresh slate! ✨ Your qubits are initialized to the ground state, |0⟩. Like a blank canvas ready for some quantum artistry! Let's apply some gates!",
            "All qubits reporting for duty! 🫡 Currently in the default |0⟩ state. This is our starting point before we dive into superposition and entanglement!"
        ]
    }
    # Use the base key (without emoji) to find the list
    base_key = state_key.split(" ")[0].lower()
    possible_explanations = explanations.get(base_key, ["Woof? I'm not sure about that state! Try another one! 🧐"])
    return random.choice(possible_explanations) # Return a random variation

# --- Helper Functions ---
def simulate_measurement(num_qubits: int, state_type: str) -> List[str]:
    """Simulates measuring qubits based on their prepared state."""
    results = []
    if state_type == STATE_SUPERPOSITION:
        # In superposition, each qubit collapses randomly to |0⟩ or |1⟩ (approx 50/50)
        results = [random.choice(["|0⟩", "|1⟩"]) for _ in range(num_qubits)]
    elif state_type == STATE_ENTANGLEMENT:
        # Simulate Bell state |Φ+⟩ = (|00⟩ + |11⟩)/√2 for simplicity if num_qubits >= 2
        if num_qubits >= 2:
            # Measure the first qubit
            first_qubit_result = random.choice(["|0⟩", "|1⟩"])
            results.append(first_qubit_result)
            # The second qubit is perfectly correlated
            results.append(first_qubit_result)
            # Any remaining qubits collapse randomly (simplified)
            results.extend([random.choice(["|0⟩", "|1⟩"]) for _ in range(num_qubits - 2)])
        else: # Only 1 qubit, can't be truly entangled in this simple model
             results = [random.choice(["|0⟩", "|1⟩"])]
    else: # Default or measured state is just classical bits
        results = [random.choice(["|0⟩", "|1⟩"]) for _ in range(num_qubits)] # Or maybe just keep previous state? Let's randomize.

    # Add some dramatic flair
    st.toast(f"Quantum Collapse! Measured: {' '.join(results)}", icon="💥")
    return results

def get_qubit_visualization(num_qubits: int, measured_results: Optional[List[str]] = None, prepared_state: str = NO_STATE) -> str:
    """Creates a simple text/emoji visualization of the qubits."""
    if measured_results:
        return " ".join(measured_results)
    elif prepared_state == STATE_SUPERPOSITION:
        return " ".join(["🌀"] * num_qubits) # Swirl emoji for superposition
    elif prepared_state == STATE_ENTANGLEMENT:
        if num_qubits >= 2:
             # Link emoji for entanglement (simplified representation)
            return "🔗".join(["✨"] * num_qubits)
        else:
            return "✨" # Can't visualize entanglement well with 1 qubit
    else: # Initialized state
        return " ".join(["|0⟩"] * num_qubits)


# --- Streamlit UI - Enhanced for Engagement and Fun ---
def main():
    st.set_page_config(
        page_title="Vers3Dynamics Quantum Lab🔬",
        page_icon="🐶", # Bo the AI Dog!
        layout="wide",
        initial_sidebar_state="expanded" # Keep sidebar open initially
    )

    # --- Session State Initialization ---
    if 'prepared_state' not in st.session_state:
        st.session_state.prepared_state = NO_STATE
    if 'measured_results' not in st.session_state:
        st.session_state.measured_results = None
    if 'num_qubits' not in st.session_state:
        st.session_state.num_qubits = 2 # Default
    if 'teleport_attempts' not in st.session_state:
         st.session_state.teleport_attempts = 0
    if 'teleport_successes' not in st.session_state:
        st.session_state.teleport_successes = 0


    # --- Header ---
    col_title, col_logo = st.columns([4, 1])
    with col_title:
        st.title("Vers3Dynamics Quantum Lab 🔬")
        st.markdown(" Unleash the power of the quantum with Obama's **Bo the AI Dog!** 🐶 Let's explore qubits, superposition, entanglement, and teleportation! 🌌")
    with col_logo:
         # Replace with an actual logo if you have one!
         st.image("quantum.jpg", width=200) # Placeholder for logo


    st.divider()

    # --- Sidebar ---
    with st.sidebar:
        st.header("About Vers3Dynamics ℹ️")
        st.info(
            "**Making Quantum Fun!** This app, founded by Christopher Woodyard, explores quantum concepts interactively. "
            "Powered by Vers3Dynamics. ⚛️"
        )
        # Let's add some fun stats here
        st.subheader("Your Quantum Journey:")
        st.write(f"Teleportation Attempts: {st.session_state.teleport_attempts}")
        st.write(f"Successful Teleports: {st.session_state.teleport_successes}")
        if st.session_state.teleport_attempts > 0:
            success_rate = (st.session_state.teleport_successes / st.session_state.teleport_attempts) * 100
            st.progress(int(success_rate))
            st.caption(f"Teleportation Success Rate: {success_rate:.1f}%")

        st.divider()
        st.audio("hello (1).mp3", format="audio/mp3") # Removed autoplay, it's often annoying
        st.markdown("[Learn about Quantum Teleportation](https://vers3dynamics.com/an-essay-towards-a-new-theory-of-ontological-fluidity-quantum-teleportation-and-the-mutable-foundations-of-reality)")
        st.markdown("[Wellness Coach](https://mnemosynehealth.streamlit.app)")
        st.divider()
        st.caption("Have a great day today")


    # --- Quantum Circuit Simulator ---
    st.header("⚛️ Quantum Playground")
    st.write("Let's create and measure quantum states!")

    # --- Qubit Setup ---
    new_num_qubits = st.slider("Select Number of Qubits (1-8):", 1, 8, st.session_state.num_qubits, key="qubit_slider")
    if new_num_qubits != st.session_state.num_qubits:
        st.session_state.num_qubits = new_num_qubits
        # Reset states if qubit number changes
        st.session_state.prepared_state = NO_STATE
        st.session_state.measured_results = None
        st.toast(f"Switched to {st.session_state.num_qubits} qubits! Resetting state.", icon="⚙️")
        time.sleep(0.5) # Allow toast to show
        st.rerun() # Rerun to update visuals immediately # <--- CORRECTED

    st.info(f"Working with **{st.session_state.num_qubits} qubits**. Bo says: '{'Woof!' * st.session_state.num_qubits}' 🐾")

    # --- State Preparation ---
    st.subheader("1. Prepare Quantum State")
    col_prep1, col_prep2 = st.columns(2)
    with col_prep1:
        prep_superposition = st.button("🌀 Put Qubits in Superposition", use_container_width=True)
        if prep_superposition:
            st.session_state.prepared_state = STATE_SUPERPOSITION
            st.session_state.measured_results = None # Clear previous measurement
            st.toast("Superposition engaged! Qubits are now fuzzy! 🌀", icon="✨")

    with col_prep2:
        # Disable entanglement button if only 1 qubit
        can_entangle = st.session_state.num_qubits >= 2
        prep_entanglement = st.button("🔗 Entangle Qubits (First Pair)", disabled=not can_entangle, use_container_width=True)
        if prep_entanglement and can_entangle:
            st.session_state.prepared_state = STATE_ENTANGLEMENT
            st.session_state.measured_results = None
            st.toast("Entanglement successful! Spooky action deployed! 🔗", icon="👻")
        elif prep_entanglement and not can_entangle:
             st.warning("Need at least 2 qubits to entangle!", icon="⚠️")


    # --- Display Current State ---
    st.subheader("Current Qubit State:")
    current_viz = get_qubit_visualization(st.session_state.num_qubits, st.session_state.measured_results, st.session_state.prepared_state)
    st.code(current_viz, language=None) # Use st.code for monospaced look

    # --- Measurement ---
    st.subheader("2. Measure Qubits")
    measure_button = st.button("💥 Measure the Qubits!", disabled=(st.session_state.prepared_state == NO_STATE), use_container_width=True)

    if measure_button and st.session_state.prepared_state != NO_STATE:
        with st.spinner("Collapsing wave functions... Measuring outcomes... 🤔"):
            time.sleep(random.uniform(0.5, 1.5)) # Simulate measurement time
            st.session_state.measured_results = simulate_measurement(st.session_state.num_qubits, st.session_state.prepared_state)
            st.session_state.prepared_state = STATE_MEASURED # Update state to measured
            st.rerun() # Rerun to show results immediately # <--- CORRECTED

    # --- Quantum Explanation ---
    st.subheader("🧠 Bo Explains...")
    # Determine which state concept to explain
    state_to_explain = st.session_state.prepared_state
    if state_to_explain == NO_STATE:
        state_to_explain = "initialized" # Give initial explanation
    elif state_to_explain == STATE_MEASURED and st.session_state.measured_results:
         # If measured, maybe explain measurement itself
         state_to_explain = STATE_MEASURED


    # Use an expander for the explanation
    with st.expander(f"Learn about {state_to_explain}", expanded=(st.session_state.prepared_state != NO_STATE)):
        with st.spinner("Asking Bo the AI Dog... 🐶 Woof woof..."):
            time.sleep(0.8) # Simulate AI thinking
            explanation = get_ai_explanation(state_to_explain)
        st.info(explanation, icon="💡")


    st.divider()

    # --- Quantum Teleportation Experiment ---
    st.header("🌌 Quantum Teleportation Experiment")
    st.write("Attempt to teleport the *state* of the first qubit (if prepared)! Requires entanglement. 💫")

    # Teleportation is only meaningful if we have a state prepared (and ideally entangled)
    can_teleport = st.session_state.prepared_state in [STATE_SUPERPOSITION, STATE_ENTANGLEMENT] and st.session_state.num_qubits >= 2

    teleport_button = st.button("🚀 Initiate Quantum Teleportation!", key="teleport_button", disabled=not can_teleport, use_container_width=True)

    if teleport_button and can_teleport:
        st.session_state.teleport_attempts += 1
        # Slightly higher chance of success if entangled? Let's add that!
        success_chance = 0.7 if st.session_state.prepared_state == STATE_ENTANGLEMENT else 0.5
        spinner_messages = [
            "Engaging Quantum Entanglers...⚙️",
            "Calibrating Spacetime Manifold...🗺️",
            "Verifying Bell State Measurement...🔔",
            "Sending Classical Correction Signal...📡",
            "Reconstructing Quantum State at Destination...✨"
        ]
        teleport_success = False
        with st.spinner(random.choice(spinner_messages)):
            time.sleep(random.uniform(1.5, 3.0)) # Simulate complex process
            teleport_success = random.random() < success_chance # Use the weighted chance

        if teleport_success:
            st.session_state.teleport_successes += 1
            st.balloons()
            success_messages = [
                "🎉 Beam me up, Scotty! Quantum state successfully teleported! ✨ You've cheated distance!",
                "✅ Phenomenal! The quantum state arrived intact across the void! Spacetime warped successfully! 🤯",
                "WOOHOO! Teleportation complete! The qubit's essence is now over *there*! ➡️",
            ]
            st.success(random.choice(success_messages), icon="✅")
            # Maybe visually show the teleported state? (Simplified)
            st.info("Imagine the first qubit's state (🌀 or ✨) is now perfectly replicated on a distant qubit!", icon="➡️")
        else:
            failure_reasons = [
                "Decoherence cascade detected! 😵 Quantum state lost to noise!",
                "Oops! Entanglement link severed prematurely! 💔 Try again!",
                "Quantum Gremlins 👾 intercepted the classical signal! Teleportation failed!",
                "Spacetime flux variance exceeded tolerance! 📉 State corrupted!",
                "Measurement error on the Bell state! 🔔 Teleportation sequence aborted!"
            ]
            st.error(f"💥 Teleportation Failed! Reason: {random.choice(failure_reasons)} Try rebuilding entanglement! 😔", icon="❌")
        # Rerun to update sidebar stats
        time.sleep(1) # Let user read the message
        st.rerun() # <--- CORRECTED

    elif teleport_button and not can_teleport:
        if st.session_state.num_qubits < 2:
             st.warning("Teleportation needs at least 2 qubits (one to send, one entangled pair minimum).", icon="⚠️")
        else:
             st.warning("Prepare a quantum state (Superposition or Entanglement) first before attempting teleportation!", icon="⚠️")


if __name__ == "__main__":
    main()
