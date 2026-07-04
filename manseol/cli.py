"""
만세력 CLI 인터페이스
사주 계산을 위한 커맨드라인 도구
"""

from datetime import datetime

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from manseol.models.input_model import CalendarType, Gender, SajuInput
from manseol.output.json_exporter import JsonExporter

console = Console()


@click.command()
@click.option("--name", "-n", required=True, help="이름")
@click.option(
    "--birth-date",
    "-d",
    required=True,
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="생년월일 (YYYY-MM-DD)",
)
@click.option("--birth-time", "-t", default=None, help="출생시간 (HH:MM). 미상시 생략")
@click.option(
    "--calendar",
    "-c",
    type=click.Choice(["solar", "lunar", "leap_lunar"]),
    default="solar",
    help="달력 유형 (solar: 양력, lunar: 음력, leap_lunar: 윤달)",
)
@click.option("--city", default="Seoul", help="출생 도시 (경도 보정용)")
@click.option("--gender", "-g", type=click.Choice(["male", "female"]), required=True, help="성별")
@click.option("--jajasi", is_flag=True, default=False, help="야자시/조자시 적용")
@click.option("--longitude", type=float, default=None, help="직접 입력 경도 (city 대신 사용)")
@click.option("--no-time-correction", is_flag=True, default=False, help="시간 보정 비활성화")
@click.option("--output", "-o", type=click.Path(), default=None, help="출력 파일 경로 (JSON)")
@click.option(
    "--format", "-f", type=click.Choice(["json", "table"]), default="table", help="출력 형식"
)
def main(
    name: str,
    birth_date: datetime,
    birth_time: str | None,
    calendar: str,
    city: str,
    gender: str,
    jajasi: bool,
    longitude: float | None,
    no_time_correction: bool,
    output: str | None,
    format: str,
):
    """
    만세력 사주 계산기

    생년월일시를 입력받아 사주팔자를 계산합니다.

    예시:
        python -m manseol.cli -n "홍길동" -d 1990-05-15 -t 14:30 -g male
    """
    try:
        # 출생시간 파싱
        parsed_time = None
        if birth_time:
            try:
                parsed_time = datetime.strptime(birth_time, "%H:%M").time()
            except ValueError:
                console.print(
                    "[red]오류: 시간 형식이 잘못되었습니다. HH:MM 형식으로 입력하세요.[/red]"
                )
                return

        # 입력 데이터 생성
        saju_input = SajuInput(
            name=name,
            birth_date=birth_date.date(),
            birth_time=parsed_time,
            calendar=CalendarType(calendar),
            city=city,
            gender=Gender(gender),
            jajasi=jajasi,
            longitude=longitude,
            apply_time_correction=not no_time_correction,
        )

        # 사주 계산
        exporter = JsonExporter(saju_input)
        result = exporter.generate_result()

        # 출력
        if format == "json" or output:
            json_str = result.to_json(indent=2)

            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(json_str)
                console.print(f"[green]결과가 {output}에 저장되었습니다.[/green]")

            if format == "json":
                console.print(json_str)
        else:
            _display_table(result)

    except Exception as e:
        console.print(f"[red]오류 발생: {e}[/red]")
        raise


def _display_table(result):
    """테이블 형식으로 결과 출력"""

    # 기본 정보
    console.print(
        Panel(
            f"[bold]{result.input.name}[/bold]의 사주명식\n"
            f"생년월일: {result.input.birth_date} "
            f"({result.input.calendar}) "
            f"{result.input.birth_time or '시간 미상'}",
            title="사주팔자",
            border_style="blue",
        )
    )

    # 시간 보정 정보
    if result.adjusted_time:
        console.print(
            f"\n[dim]시간 보정: {result.adjusted_time.total_correction_minutes:+.1f}분[/dim]"
        )
        console.print(f"[dim]진태양시: {result.adjusted_time.true_solar_time}[/dim]")

    # 사주 4주 테이블
    pillars_table = Table(title="\n사주 4주(四柱)", show_header=True)
    pillars_table.add_column("", style="dim")
    pillars_table.add_column("년주(年柱)", justify="center")
    pillars_table.add_column("월주(月柱)", justify="center")
    pillars_table.add_column("일주(日柱)", justify="center")

    if result.pillars.hour:
        pillars_table.add_column("시주(時柱)", justify="center")

    # 천간
    row_stem = ["천간"]
    row_stem.append(f"{result.pillars.year.stem.chinese}\n({result.pillars.year.stem.korean})")
    row_stem.append(f"{result.pillars.month.stem.chinese}\n({result.pillars.month.stem.korean})")
    row_stem.append(f"{result.pillars.day.stem.chinese}\n({result.pillars.day.stem.korean})")
    if result.pillars.hour:
        row_stem.append(f"{result.pillars.hour.stem.chinese}\n({result.pillars.hour.stem.korean})")
    pillars_table.add_row(*row_stem)

    # 지지
    row_branch = ["지지"]
    row_branch.append(
        f"{result.pillars.year.branch.chinese}\n({result.pillars.year.branch.korean})"
    )
    row_branch.append(
        f"{result.pillars.month.branch.chinese}\n({result.pillars.month.branch.korean})"
    )
    row_branch.append(f"{result.pillars.day.branch.chinese}\n({result.pillars.day.branch.korean})")
    if result.pillars.hour:
        row_branch.append(
            f"{result.pillars.hour.branch.chinese}\n({result.pillars.hour.branch.korean})"
        )
    pillars_table.add_row(*row_branch)

    # 십성
    row_ten_god = ["십성"]
    row_ten_god.append(result.pillars.year.ten_god or "-")
    row_ten_god.append(result.pillars.month.ten_god or "-")
    row_ten_god.append("일간")
    if result.pillars.hour:
        row_ten_god.append(result.pillars.hour.ten_god or "-")
    pillars_table.add_row(*row_ten_god)

    # 12운성
    row_phase = ["12운성"]
    row_phase.append(result.pillars.year.twelve_phase or "-")
    row_phase.append(result.pillars.month.twelve_phase or "-")
    row_phase.append(result.pillars.day.twelve_phase or "-")
    if result.pillars.hour:
        row_phase.append(result.pillars.hour.twelve_phase or "-")
    pillars_table.add_row(*row_phase)

    console.print(pillars_table)

    # 일간 분석
    console.print(
        Panel(
            f"[bold]{result.analysis.day_master.chinese}({result.analysis.day_master.korean})[/bold] - "
            f"{result.analysis.day_master.element} {result.analysis.day_master.polarity}\n"
            f"물상: {result.analysis.day_master.metaphor}",
            title="일간(日干) 분석",
            border_style="green",
        )
    )

    # 오행 분포
    elements_table = Table(title="\n오행 분포", show_header=True)
    elements_table.add_column("목(木)", justify="center")
    elements_table.add_column("화(火)", justify="center")
    elements_table.add_column("토(土)", justify="center")
    elements_table.add_column("금(金)", justify="center")
    elements_table.add_column("수(水)", justify="center")

    elements_table.add_row(
        f"{result.analysis.five_elements.wood}\n({result.analysis.five_elements.distribution.get('목', 0)}%)",
        f"{result.analysis.five_elements.fire}\n({result.analysis.five_elements.distribution.get('화', 0)}%)",
        f"{result.analysis.five_elements.earth}\n({result.analysis.five_elements.distribution.get('토', 0)}%)",
        f"{result.analysis.five_elements.metal}\n({result.analysis.five_elements.distribution.get('금', 0)}%)",
        f"{result.analysis.five_elements.water}\n({result.analysis.five_elements.distribution.get('수', 0)}%)",
    )
    console.print(elements_table)

    # 신강/신약
    strength_color = (
        "green"
        if result.analysis.strength.level == "신강"
        else "red"
        if result.analysis.strength.level == "신약"
        else "yellow"
    )
    console.print(
        f"\n신강/신약: [{strength_color}]{result.analysis.strength.level}[/{strength_color}] "
        f"(점수: {result.analysis.strength.score})"
    )

    # 용신
    console.print(
        f"용신: [bold]{result.analysis.useful_god.primary}[/bold] ({result.analysis.useful_god.type})"
    )
    if result.analysis.useful_god.secondary:
        console.print(f"희신: {result.analysis.useful_god.secondary}")

    # 신살
    if result.analysis.shensha:
        console.print("\n[bold]신살:[/bold]")
        for s in result.analysis.shensha:
            color = "green" if s.type == "길신" else "red" if s.type == "흉신" else "yellow"
            console.print(f"  [{color}]{s.name}[/{color}] ({s.position}) - {s.description}")

    # 대운
    if result.fortune_cycles:
        console.print(
            f"\n[bold]대운[/bold] (시작: {result.fortune_cycles.start_age}세, {result.fortune_cycles.direction})"
        )

        daewun_table = Table(show_header=True)
        daewun_table.add_column("나이", justify="center")
        daewun_table.add_column("대운", justify="center")
        daewun_table.add_column("십성", justify="center")
        daewun_table.add_column("12운성", justify="center")

        for cycle in result.fortune_cycles.cycles[:8]:  # 8개만 표시
            daewun_table.add_row(
                f"{cycle.start_age}-{cycle.end_age}",
                f"{cycle.ganji_chinese}\n({cycle.ganji_korean})",
                cycle.ten_god,
                cycle.twelve_phase,
            )

        console.print(daewun_table)


if __name__ == "__main__":
    main()
