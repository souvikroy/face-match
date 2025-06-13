# Face Trait Matcher (Experimental)

This project provides a FastAPI service that attempts to match psychological traits from a provided `traits.json` file to uploaded face images. **This approach is highly speculative and lacks scientific support.** Results may be biased and should **not** be used for high‑stakes or real‑world decisions.

## Ethical Disclaimer
Inferring psychological traits solely from facial appearance is not scientifically validated and can reinforce harmful stereotypes. The system presented here is for experimental and educational purposes only. Output should be treated with extreme caution.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY=your-key
   ```
3. Run the server:
   ```bash
   uvicorn app.api.main:app --reload
   ```

## Usage
Send a POST request to `/analyze_face_traits` with an image file under the `file` field. The response includes extracted tags, predicted traits with similarity scores, and reasoning from both the matcher and verifier agents.

## Limitations
- Face detection and emotion recognition may be inaccurate.
- Trait inference is speculative and biased.
- The verifier agent only provides heuristic feedback and does not validate predictions scientifically.

**Use responsibly and only for demonstration purposes.**
