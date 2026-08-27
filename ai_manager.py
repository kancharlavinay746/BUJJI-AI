import os
from dotenv import load_dotenv
from ollama import chat
from groq import Groq

load_dotenv()


class AIManager:

    def __init__(self):

        self.ollama_model = "llama3.2:3b"

        groq_key = os.getenv("GROQ_API_KEY")

        self.groq = Groq(
            api_key=groq_key
        ) if groq_key else None

        print("\n" + "=" * 50)
        print("🧠 BUJJI AI MANAGER")
        print("=" * 50)
        print("🟢 Ollama :", self.ollama_model)
        print(
            "🔵 Groq   :",
            "READY" if self.groq else "NOT CONFIGURED"
        )
        print("=" * 50)

    # -----------------------------------------
    # OLLAMA
    # -----------------------------------------

    def ask_ollama(self, prompt):

        response = chat(
            model=self.ollama_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are BUJJI, a smart Windows "
                        "desktop AI assistant. "
                        "Understand natural language. "
                        "Be concise and helpful."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"].strip()

    # -----------------------------------------
    # GROQ
    # -----------------------------------------

    def ask_groq(self, prompt):

        if not self.groq:
            raise RuntimeError(
                "Groq API key not configured."
            )

        response = self.groq.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are BUJJI, an intelligent "
                        "Windows desktop assistant. "
                        "Understand natural language "
                        "and answer concisely."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2,
            max_tokens=1024
        )

        return response.choices[0].message.content.strip()

    # -----------------------------------------
    # SMART AI
    # -----------------------------------------

    def ask(self, prompt):

        print(f"\n🧠 AI Request: {prompt}")

        # Groq first
        if self.groq:

            try:

                print("🔵 Using Groq...")

                result = self.ask_groq(prompt)

                print("✅ Groq response received.")

                return result

            except Exception as e:

                print(
                    f"⚠️ Groq failed: {e}"
                )

        # Ollama fallback
        try:

            print("🟢 Using Ollama...")

            result = self.ask_ollama(prompt)

            print(
                "✅ Ollama response received."
            )

            return result

        except Exception as e:

            print(
                f"❌ Ollama failed: {e}"
            )

            return (
                "Sorry, my AI systems are "
                "currently unavailable."
            )

    # -----------------------------------------
    # STATUS
    # -----------------------------------------

    def status(self):

        return {
            "ollama": True,
            "groq": self.groq is not None
        }


# ---------------------------------------------
# GLOBAL INSTANCE
# ---------------------------------------------

ai_manager = AIManager()