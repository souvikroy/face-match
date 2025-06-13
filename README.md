# Face Trait Matcher (Experimental)

This project provides a FastAPI service that attempts to match psychological traits from a provided `traits.json` file to uploaded face images. **This approach is highly speculative and lacks scientific support.** Results may be biased and should **not** be used for high‑stakes or real‑world decisions. Every API response includes a disclaimer reiterating these limitations.

## Ethical Disclaimer
Inferring psychological traits solely from facial appearance is not scientifically validated and can reinforce harmful stereotypes. The system presented here is for experimental and educational purposes only. Output should be treated with extreme caution.

## Setup
1. Install dependencies (you can run the provided helper script):
   ```bash
   ./setup.sh
   ```
2. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY=your-key
   ```
3. Run the server:
   ```bash
   uvicorn app.api.main:app --reload
   ```
4. Run the tests (requires the dependencies above):
   ```bash
   pytest -q
   ```

## Usage
Send a POST request to `/analyze_face_traits` with an image file under the `file` field. The response includes extracted tags, predicted traits with similarity scores, and reasoning from both the matcher and verifier agents.

## Limitations
- Face detection and emotion recognition may be inaccurate.
- Trait inference is speculative and biased.
- The verifier agent only provides heuristic feedback and does not validate predictions scientifically.

**Use responsibly and only for demonstration purposes.**
