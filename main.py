import asyncio
from dotenv import load_dotenv
from livekit.agents import JobContext, AutoSubscribe, Worker, cli, llm, WorkerOptions
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import silero, openai
from api import AssistantFunc 


load_dotenv()


async def entrypoint(ctx: JobContext):
    initial_ctx = llm.chat_context.append(
        role = "system",
        text = "You are a voice assistant created for Lohit. Act like his day to day assistant and friend"
    )

    await ctx.connect(auto_subsctibe = AutoSubscribe.AUDIO_ONLY)
    fnc_ctx = AssistantFunc()


    assistant = VoiceAssistant (
        vad = silero.VAD.load(),
        stt = openai.STT(),
        llm = openai.LLM(),
        tts = openai.TTS(),
        chat_ctx = initial_ctx,
        fnc_ctx= fnc_ctx
    )
    assistant.start(ctx.room)

    await asyncio.sleep(1)
    await assistant.say("Hey Lohi, How can I help you today !!",allow_interruptions=True)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))

