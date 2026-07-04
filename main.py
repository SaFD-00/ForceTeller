#!/usr/bin/env python3
"""
ForceTeller 통합 진입점
사주명리학 만세력 계산 및 AI 해석 시스템

Usage:
    # CLI 모드 (사주 계산)
    python main.py cli --name "홍길동" --birth-date 1990-05-15 --birth-time 14:30 --gender male

    # API 서버 실행
    python main.py server --host 0.0.0.0 --port 8000

    # 대화형 모드
    python main.py interactive
"""

import asyncio
from datetime import datetime

import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()


@click.group()
@click.version_option(version="1.0.0", prog_name="ForceTeller")
def main():
    """🔮 ForceTeller: 사주명리학 만세력 계산 및 AI 해석 시스템"""
    pass


@main.command()
@click.option("--name", "-n", required=True, help="이름")
@click.option("--birth-date", "-d", required=True, help="생년월일 (YYYY-MM-DD)")
@click.option("--birth-time", "-t", default=None, help="출생시간 (HH:MM)")
@click.option("--calendar", "-c", default="solar", help="달력 유형 (solar/lunar/leap_lunar)")
@click.option("--city", default="Seoul", help="출생 도시")
@click.option("--gender", "-g", required=True, help="성별 (male/female)")
@click.option("--jajasi", is_flag=True, help="야자시/조자시 적용")
@click.option("--output", "-o", default=None, help="출력 파일 경로")
@click.option("--format", "-f", default="table", help="출력 형식 (json/table)")
def cli(name, birth_date, birth_time, calendar, city, gender, jajasi, output, format):
    """CLI 모드: 사주 계산"""
    from manseol.cli import main as cli_main

    # Click 컨텍스트로 CLI 실행
    ctx = click.Context(cli_main)
    ctx.invoke(
        cli_main,
        name=name,
        birth_date=datetime.strptime(birth_date, "%Y-%m-%d"),
        birth_time=birth_time,
        calendar=calendar,
        city=city,
        gender=gender,
        jajasi=jajasi,
        output=output,
        format=format,
    )


@main.command()
@click.option("--host", "-h", default="127.0.0.1", help="서버 호스트")
@click.option("--port", "-p", default=8000, type=int, help="서버 포트")
@click.option("--reload", is_flag=True, help="자동 리로드 활성화")
def server(host, port, reload):
    """API 서버 실행"""
    from api.server import run_server

    console.print(
        Panel(
            f"🔮 ForceTeller API 서버\n"
            f"📍 http://{host}:{port}\n"
            f"📚 API 문서: http://{host}:{port}/docs",
            title="서버 시작",
            border_style="green",
        )
    )

    run_server(host=host, port=port, reload=reload)


@main.command()
def interactive():
    """대화형 모드: 사주 입력 후 AI와 대화"""
    asyncio.run(_interactive_mode())


async def _interactive_mode():
    """대화형 모드 실행"""
    from agents.orchestrator import Orchestrator
    from conversation.session_manager import SessionManager
    from manseol.models.input_model import Gender, SajuInput
    from manseol.output.json_exporter import JsonExporter

    console.print(
        Panel(
            "🔮 ForceTeller 대화형 모드\n"
            "사주 정보를 입력하고 AI와 대화하세요.\n"
            "종료하려면 'quit' 또는 'exit'를 입력하세요.",
            title="환영합니다",
            border_style="blue",
        )
    )

    # 사주 정보 입력
    console.print("\n[bold]사주 정보 입력[/bold]")

    name = Prompt.ask("이름")
    birth_date_str = Prompt.ask("생년월일 (YYYY-MM-DD)")
    birth_time_str = Prompt.ask("출생시간 (HH:MM, 미상시 Enter)", default="")
    gender_str = Prompt.ask("성별", choices=["male", "female"])
    city = Prompt.ask("출생 도시", default="Seoul")

    try:
        # 날짜 파싱
        birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()

        # 시간 파싱
        birth_time = None
        if birth_time_str:
            birth_time = datetime.strptime(birth_time_str, "%H:%M").time()

        # 사주 계산
        console.print("\n[dim]사주 계산 중...[/dim]")

        saju_input = SajuInput(
            name=name,
            birth_date=birth_date,
            birth_time=birth_time,
            gender=Gender(gender_str),
            city=city,
        )

        exporter = JsonExporter(saju_input)
        result = exporter.generate_result()
        saju_data = result.to_dict()

        # 간단한 사주 정보 표시
        pillars = result.pillars
        console.print(
            Panel(
                f"년주: {pillars.year.ganji_chinese} ({pillars.year.ganji_korean})\n"
                f"월주: {pillars.month.ganji_chinese} ({pillars.month.ganji_korean})\n"
                f"일주: {pillars.day.ganji_chinese} ({pillars.day.ganji_korean})\n"
                f"시주: {pillars.hour.ganji_chinese if pillars.hour else '미상'} "
                f"({pillars.hour.ganji_korean if pillars.hour else ''})",
                title=f"{name}님의 사주",
                border_style="green",
            )
        )

        # 세션 및 오케스트레이터 초기화
        session_manager = SessionManager()
        session = session_manager.create_session(saju_data)
        orchestrator = Orchestrator()

        console.print("\n[bold green]대화를 시작합니다. 질문을 입력하세요.[/bold green]")
        console.print("[dim]예: '제 성격에 대해 알려주세요', '올해 운세는 어때요?'[/dim]\n")

        # 대화 루프
        while True:
            try:
                user_input = Prompt.ask("[bold blue]질문[/bold blue]")

                if user_input.lower() in ["quit", "exit", "종료", "나가기"]:
                    console.print("\n[yellow]대화를 종료합니다. 감사합니다! 🙏[/yellow]")
                    break

                if not user_input.strip():
                    continue

                # 사용자 메시지 기록
                session.add_user_message(user_input)

                # 해석 요청
                console.print("[dim]해석 중...[/dim]")

                result = await orchestrator.route_and_interpret(
                    saju_data=saju_data,
                    question=user_input,
                    conversation_history=session.get_messages_for_llm(),
                    include_synthesis=True,
                )

                # 응답 출력
                if result.get("synthesis"):
                    response_text = result["synthesis"]["interpretation"]
                else:
                    first_interp = list(result["interpretations"].values())[0]
                    response_text = first_interp.get("interpretation", "")

                console.print(Panel(response_text, title="🔮 해석", border_style="magenta"))

                # 어시스턴트 메시지 기록
                session.add_assistant_message(response_text)

                # 사용된 에이전트 표시
                agents_used = result.get("agents_used", [])
                if agents_used:
                    console.print(f"[dim]사용된 에이전트: {', '.join(agents_used)}[/dim]\n")

            except KeyboardInterrupt:
                console.print("\n[yellow]대화를 종료합니다.[/yellow]")
                break
            except Exception as e:
                console.print(f"[red]오류: {str(e)}[/red]")

    except ValueError as e:
        console.print(f"[red]입력 오류: {str(e)}[/red]")
    except Exception as e:
        console.print(f"[red]오류 발생: {str(e)}[/red]")


@main.command()
def info():
    """시스템 정보 표시"""
    from config.settings import settings

    key_status = "설정됨" if settings.OPENROUTER_API_KEY else "미설정"
    console.print(
        Panel(
            f"[bold]ForceTeller[/bold] v1.0.0\n\n"
            f"📦 만세력 계산 엔진 + AI 해석 에이전트\n\n"
            f"[bold]LLM 설정 (OpenRouter):[/bold]\n"
            f"  • API Key: {key_status}\n"
            f"  • 기본 모델: {settings.OPENROUTER_MODEL}\n"
            f"  • 라우팅 모델: {settings.OPENROUTER_ROUTING_MODEL}\n"
            f"  • 폴백 모델: {settings.OPENROUTER_FALLBACK_MODEL}\n\n"
            f"[bold]API 서버:[/bold]\n"
            f"  • Host: {settings.API_HOST}\n"
            f"  • Port: {settings.API_PORT}\n\n"
            f"[bold]사용법:[/bold]\n"
            f"  python main.py cli --help     CLI 도움말\n"
            f"  python main.py server         API 서버 실행\n"
            f"  python main.py interactive    대화형 모드",
            title="시스템 정보",
            border_style="blue",
        )
    )


if __name__ == "__main__":
    main()
