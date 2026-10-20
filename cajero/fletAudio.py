import asyncio
import os
from typing import Optional

import flet as ft
import flet_audio as fta


def format_time(millis: int) -> str:
    """Formatea milisegundos a formato MM:SS."""
    seconds = int(millis // 1000)
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02d}:{secs:02d}"


async def main(page: ft.Page):
    # --- Configuración visual de la página en Flet 1.0.3 ---
    page.title = "Flet 1.0.3 - Audio Studio & SFX Showcase"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 30
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#0D1117"

    # =========================================================================
    # 1. SERVICIOS DE AUDIO (flet-audio 1.0.3)
    # =========================================================================
    # IMPORTANTE en Flet 1.0+:
    # 1. Audio es una subclase de ft.Service y se auto-registra en la página.
    #    ¡Ya NO debe agregarse a page.overlay!
    # 2. Los métodos play(), pause(), resume(), seek(), etc. son CORRUTINAS
    #    (async) y deben ejecutarse con 'await'.
    # 3. Para efectos de sonido (SFX) usamos ReleaseMode.STOP para que el buffer
    #    quede en memoria y el sonido suene instantáneo en cada clic sin latencia.
    # 4. Para música o pistas de fondo usamos ReleaseMode.LOOP.
    # =========================================================================

    # Fuentes locales y remotas
    # Si existen los archivos en assets/audio se usan rutas relativas (/audio/...),
    # de lo contrario se usan URLs públicas probadas.
    AUDIO_CLICK = "/audio/click.wav" if os.path.exists("assets/audio/click.wav") else "https://codeskulptor-demos.commondatastorage.googleapis.com/pang/pop.mp3"
    AUDIO_BOING = "/audio/boing.wav" if os.path.exists("assets/audio/boing.wav") else "https://actions.google.com/sounds/v1/cartoon/cartoon_boing.ogg"
    AUDIO_MAGIC = "/audio/magic.wav" if os.path.exists("assets/audio/magic.wav") else "https://actions.google.com/sounds/v1/cartoon/magic_chime.ogg"
    AUDIO_SUCCESS = "/audio/success.wav" if os.path.exists("assets/audio/success.wav") else "https://actions.google.com/sounds/v1/cartoon/pop.ogg"
    AUDIO_MUSIC_LOCAL = "/audio/ambient.wav" if os.path.exists("assets/audio/ambient.wav") else None
    AUDIO_MUSIC_REMOTE = "https://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3"

    # Inicialización de controles Audio
    audio_click = fta.Audio(src=AUDIO_CLICK, volume=0.85, release_mode=fta.ReleaseMode.STOP)
    audio_boing = fta.Audio(src=AUDIO_BOING, volume=0.85, release_mode=fta.ReleaseMode.STOP)
    audio_magic = fta.Audio(src=AUDIO_MAGIC, volume=0.85, release_mode=fta.ReleaseMode.STOP)
    audio_success = fta.Audio(src=AUDIO_SUCCESS, volume=0.9, release_mode=fta.ReleaseMode.STOP)

    # Reproductor principal continuo
    audio_player = fta.Audio(
        src=AUDIO_MUSIC_LOCAL or AUDIO_MUSIC_REMOTE,
        volume=0.6,
        release_mode=fta.ReleaseMode.LOOP,
    )

    # Mantenemos las referencias activas en page para evitar recolección de basura
    page._audio_services = [audio_click, audio_boing, audio_magic, audio_success, audio_player]

    # =========================================================================
    # SECCIÓN 1: EFECTOS DE SONIDO E INTERACCIÓN UI (FEEDBACK AUDITIVO)
    # =========================================================================
    clicks_count = 0
    txt_clicks_counter = ft.Text("0 clics", size=13, weight=ft.FontWeight.BOLD, color="#00E8C6")

    async def on_click_button(e):
        nonlocal clicks_count
        clicks_count += 1
        txt_clicks_counter.value = f"{clicks_count} clics"
        # ¡CORRECCIÓN CLAVE!: En Flet 1.0.3 se debe await play()
        await audio_click.play()
        page.update()

    # Botón con animación de resorte (Boing)
    icono_cohete = ft.Container(
        content=ft.Icon(ft.Icons.ROCKET_LAUNCH_ROUNDED, size=36, color="#FF9100"),
        scale=ft.Scale(1.0),
        animate_scale=ft.Animation(300, ft.AnimationCurve.ELASTIC_OUT),
        alignment=ft.Alignment.CENTER,
    )

    async def on_boing_button(e):
        # 1. Reproducir sonido SFX
        await audio_boing.play()
        # 2. Animación de rebote
        icono_cohete.scale = ft.Scale(1.4)
        page.update()
        await asyncio.sleep(0.18)
        icono_cohete.scale = ft.Scale(1.0)
        page.update()

    # Tarjeta mágica con rotación y brillo (Magic Chime)
    tarjeta_magica = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.AUTO_AWESOME_ROUNDED, color="#FFD700", size=24),
                ft.Text("¡Hechizo Activo!", size=13, weight=ft.FontWeight.W_600, color="#FFD700"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        ),
        padding=ft.Padding.symmetric(horizontal=16, vertical=10),
        border_radius=10,
        border=ft.Border.all(1.2, "#FFD700"),
        bgcolor="#26200A",
        scale=ft.Scale(1.0),
        rotate=ft.Rotate(0),
        animate_scale=ft.Animation(280, ft.AnimationCurve.EASE_OUT_BACK),
        animate_rotation=ft.Animation(280, ft.AnimationCurve.EASE_IN_OUT),
        alignment=ft.Alignment.CENTER,
    )
    rotacion_magica = 0.0

    async def on_magic_button(e):
        nonlocal rotacion_magica
        # Sonido mágico
        await audio_magic.play()
        rotacion_magica = 0.12 if rotacion_magica == 0.0 else 0.0
        tarjeta_magica.scale = ft.Scale(1.15)
        tarjeta_magica.rotate = ft.Rotate(rotacion_magica)
        page.update()
        await asyncio.sleep(0.2)
        tarjeta_magica.scale = ft.Scale(1.0)
        page.update()

    # Logro / Success Chime
    badge_logro = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.VERIFIED_ROUNDED, color="#00E676", size=24),
                ft.Text("Nivel Completado", size=13, weight=ft.FontWeight.W_600, color="#00E676"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        ),
        padding=ft.Padding.symmetric(horizontal=16, vertical=10),
        border_radius=10,
        border=ft.Border.all(1.2, "#00E676"),
        bgcolor="#0A2416",
        scale=ft.Scale(1.0),
        animate_scale=ft.Animation(280, ft.AnimationCurve.ELASTIC_OUT),
        alignment=ft.Alignment.CENTER,
    )

    async def on_success_button(e):
        await audio_success.play()
        badge_logro.scale = ft.Scale(1.2)
        page.update()
        await asyncio.sleep(0.22)
        badge_logro.scale = ft.Scale(1.0)
        page.update()

    def build_sfx_tile(title: str, subtitle: str, button_text: str, button_icon: str, on_click_handler, extra_widget, accent_color: str):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(button_icon, color=accent_color, size=20),
                                bgcolor=ft.Colors.with_opacity(0.12, accent_color),
                                padding=8,
                                border_radius=8,
                            ),
                            ft.Column(
                                [
                                    ft.Text(title, size=15, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                    ft.Text(subtitle, size=12, color="#8B949E"),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Divider(height=12, color="#21262D"),
                    ft.Row(
                        [
                            ft.Button(
                                button_text,
                                icon=button_icon,
                                on_click=on_click_handler,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.with_opacity(0.18, accent_color),
                                    color=accent_color,
                                    side=ft.BorderSide(1, accent_color),
                                    padding=ft.Padding.symmetric(horizontal=14, vertical=10),
                                ),
                            ),
                            extra_widget,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                spacing=8,
            ),
            padding=16,
            border_radius=14,
            bgcolor="#161B22",
            border=ft.Border.all(1, "#30363D"),
            shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.with_opacity(0.15, "#000000")),
            expand=True,
        )

    grid_sfx = ft.Column(
        [
            ft.Row(
                [
                    build_sfx_tile(
                        title="UI Click Feedback",
                        subtitle="Respuesta táctil auditiva inmediata",
                        button_text="Pulsar Botón",
                        button_icon=ft.Icons.ADS_CLICK_ROUNDED,
                        on_click_handler=on_click_button,
                        extra_widget=ft.Container(
                            content=txt_clicks_counter,
                            bgcolor="#0A2222",
                            padding=ft.Padding.symmetric(horizontal=12, vertical=6),
                            border_radius=20,
                            border=ft.Border.all(1, "#00E8C6"),
                        ),
                        accent_color="#00E8C6",
                    ),
                    build_sfx_tile(
                        title="Rebote Elástico",
                        subtitle="Sincronizado con curvas de escala",
                        button_text="Despegar",
                        button_icon=ft.Icons.ROCKET_ROUNDED,
                        on_click_handler=on_boing_button,
                        extra_widget=icono_cohete,
                        accent_color="#FF9100",
                    ),
                ],
                spacing=16,
            ),
            ft.Row(
                [
                    build_sfx_tile(
                        title="Efecto Mágico",
                        subtitle="Campanada mágica y rotación de tarjeta",
                        button_text="Lanzar Hechizo",
                        button_icon=ft.Icons.AUTO_AWESOME_ROUNDED,
                        on_click_handler=on_magic_button,
                        extra_widget=tarjeta_magica,
                        accent_color="#FFD700",
                    ),
                    build_sfx_tile(
                        title="Éxito / Logro",
                        subtitle="Acorde armónico de confirmación",
                        button_text="Completar",
                        button_icon=ft.Icons.CHECK_CIRCLE_ROUNDED,
                        on_click_handler=on_success_button,
                        extra_widget=badge_logro,
                        accent_color="#00E676",
                    ),
                ],
                spacing=16,
            ),
        ],
        spacing=16,
    )

    # =========================================================================
    # SECCIÓN 2: REPRODUCTOR DE MÚSICA & AUDIO CONTINUO (PLAY, PAUSE, SEEK, VOL)
    # =========================================================================
    is_playing = False
    duration_millis = 0
    current_position_millis = 0
    is_seeking = False

    # Visualizador de ondas sonoras animadas
    barras_ecualizador = [
        ft.Container(width=4, height=12, bgcolor="#58A6FF", border_radius=2, animate=ft.Animation(150, ft.AnimationCurve.EASE_IN_OUT))
        for _ in range(5)
    ]

    async def animar_ecualizador():
        alturas = [
            [24, 12, 32, 18, 28],
            [14, 28, 16, 30, 10],
            [30, 18, 12, 22, 32],
            [10, 24, 30, 14, 20],
        ]
        i = 0
        while is_playing:
            for b_idx, b in enumerate(barras_ecualizador):
                b.height = alturas[i % len(alturas)][b_idx]
            page.update()
            await asyncio.sleep(0.18)
            i += 1
        # Reposo
        for b in barras_ecualizador:
            b.height = 10
        page.update()

    txt_estado = ft.Text("DETENIDO", size=11, weight=ft.FontWeight.BOLD, color="#8B949E")
    badge_estado = ft.Container(
        content=ft.Row(
            [
                ft.Container(width=8, height=8, border_radius=4, bgcolor="#8B949E"),
                txt_estado,
            ],
            spacing=6,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        bgcolor="#1C2128",
        padding=ft.Padding.symmetric(horizontal=10, vertical=4),
        border_radius=20,
        border=ft.Border.all(1, "#30363D"),
    )

    lbl_tiempo_actual = ft.Text("00:00", size=12, color="#8B949E")
    lbl_tiempo_total = ft.Text("00:00", size=12, color="#8B949E")

    slider_progreso = ft.Slider(
        min=0.0,
        max=100.0,
        value=0.0,
        active_color="#58A6FF",
        inactive_color="#21262D",
    )

    async def on_slider_change_start(e):
        nonlocal is_seeking
        is_seeking = True

    async def on_slider_change_end(e):
        nonlocal is_seeking
        if duration_millis > 0:
            target_ms = int(e.control.value)
            await audio_player.seek(ft.Duration(milliseconds=target_ms))
        is_seeking = False

    slider_progreso.on_change_start = on_slider_change_start
    slider_progreso.on_change_end = on_slider_change_end

    # Eventos nativos de flet_audio
    def on_audio_state_change(e: fta.AudioStateChangeEvent):
        nonlocal is_playing
        # En flet-audio 1.0.3, e.state es un AudioState (PLAYING, PAUSED, STOPPED, etc.)
        estado = e.state
        if estado == fta.AudioState.PLAYING:
            is_playing = True
            txt_estado.value = "REPRODUCIENDO"
            txt_estado.color = "#00E676"
            badge_estado.content.controls[0].bgcolor = "#00E676"
            badge_estado.border = ft.Border.all(1, "#00E676")
            btn_play_pause.icon = ft.Icons.PAUSE_ROUNDED
            btn_play_pause.tooltip = "Pausar"
            asyncio.create_task(animar_ecualizador())
        elif estado == fta.AudioState.PAUSED:
            is_playing = False
            txt_estado.value = "PAUSADO"
            txt_estado.color = "#FFB74D"
            badge_estado.content.controls[0].bgcolor = "#FFB74D"
            badge_estado.border = ft.Border.all(1, "#FFB74D")
            btn_play_pause.icon = ft.Icons.PLAY_ARROW_ROUNDED
            btn_play_pause.tooltip = "Reanudar"
        elif estado in (fta.AudioState.STOPPED, fta.AudioState.COMPLETED):
            is_playing = False
            txt_estado.value = "DETENIDO"
            txt_estado.color = "#8B949E"
            badge_estado.content.controls[0].bgcolor = "#8B949E"
            badge_estado.border = ft.Border.all(1, "#30363D")
            btn_play_pause.icon = ft.Icons.PLAY_ARROW_ROUNDED
            btn_play_pause.tooltip = "Reproducir"
        page.update()

    def on_duration_change(e: fta.AudioDurationChangeEvent):
        nonlocal duration_millis
        # e.duration es un ft.Duration
        duration_millis = e.duration.in_milliseconds
        lbl_tiempo_total.value = format_time(duration_millis)
        slider_progreso.max = max(1.0, float(duration_millis))
        page.update()

    def on_position_change(e: fta.AudioPositionChangeEvent):
        nonlocal current_position_millis
        if not is_seeking:
            current_position_millis = e.position
            lbl_tiempo_actual.value = format_time(current_position_millis)
            if duration_millis > 0:
                slider_progreso.value = min(float(current_position_millis), slider_progreso.max)
            page.update()

    audio_player.on_state_change = on_audio_state_change
    audio_player.on_duration_change = on_duration_change
    audio_player.on_position_change = on_position_change

    # Controles de Reproducción
    async def toggle_play_pause(e):
        if is_playing:
            await audio_player.pause()
        else:
            if txt_estado.value == "PAUSADO":
                await audio_player.resume()
            else:
                await audio_player.play()
        page.update()

    async def stop_player(e):
        # flet-audio implementa pausa o release para detener
        await audio_player.pause()
        await audio_player.seek(ft.Duration(milliseconds=0))
        slider_progreso.value = 0.0
        lbl_tiempo_actual.value = "00:00"
        on_audio_state_change(fta.AudioStateChangeEvent(control=audio_player, state=fta.AudioState.STOPPED))
        page.update()

    btn_play_pause = ft.IconButton(
        icon=ft.Icons.PLAY_ARROW_ROUNDED,
        icon_color="#0D1117",
        bgcolor="#58A6FF",
        icon_size=32,
        tooltip="Reproducir",
        on_click=toggle_play_pause,
    )

    btn_stop = ft.IconButton(
        icon=ft.Icons.STOP_ROUNDED,
        icon_color="#E6EDF3",
        bgcolor="#21262D",
        icon_size=24,
        tooltip="Detener",
        on_click=stop_player,
    )

    # Control de volumen
    volumen_actual = 0.6
    volumen_previo = 0.6
    txt_volumen = ft.Text("60%", size=12, color="#C9D1D9")

    btn_mute = ft.IconButton(
        icon=ft.Icons.VOLUME_UP_ROUNDED,
        icon_color="#58A6FF",
        icon_size=22,
        tooltip="Silenciar / Activar sonido",
    )

    def actualizar_icono_volumen(vol: float):
        if vol <= 0.001:
            btn_mute.icon = ft.Icons.VOLUME_OFF_ROUNDED
            btn_mute.icon_color = "#8B949E"
        elif vol < 0.4:
            btn_mute.icon = ft.Icons.VOLUME_DOWN_ROUNDED
            btn_mute.icon_color = "#58A6FF"
        else:
            btn_mute.icon = ft.Icons.VOLUME_UP_ROUNDED
            btn_mute.icon_color = "#58A6FF"

    async def on_volume_slider_change(e):
        nonlocal volumen_actual, volumen_previo
        volumen_actual = round(e.control.value, 2)
        if volumen_actual > 0:
            volumen_previo = volumen_actual
        audio_player.volume = volumen_actual
        audio_player.update()
        txt_volumen.value = f"{int(volumen_actual * 100)}%"
        actualizar_icono_volumen(volumen_actual)
        page.update()

    slider_volumen = ft.Slider(
        min=0.0,
        max=1.0,
        divisions=20,
        value=0.6,
        active_color="#58A6FF",
        inactive_color="#21262D",
        on_change=on_volume_slider_change,
        expand=True,
    )

    async def on_toggle_mute(e):
        nonlocal volumen_actual
        if volumen_actual > 0:
            volumen_actual = 0.0
        else:
            volumen_actual = volumen_previo or 0.6
        slider_volumen.value = volumen_actual
        audio_player.volume = volumen_actual
        audio_player.update()
        txt_volumen.value = f"{int(volumen_actual * 100)}%"
        actualizar_icono_volumen(volumen_actual)
        page.update()

    btn_mute.on_click = on_toggle_mute

    # Selector de pista (Local vs Remoto)
    lbl_pista_activa = ft.Text(
        "Pista: Ambient Synthesizer (Local Asset)" if AUDIO_MUSIC_LOCAL else "Pista: Soundtrack Stream (Cloud URL)",
        size=13,
        weight=ft.FontWeight.W_500,
        color="#E6EDF3",
    )

    async def cambiar_fuente_audio(e):
        opcion = e.control.value
        if opcion == "local" and AUDIO_MUSIC_LOCAL:
            audio_player.src = AUDIO_MUSIC_LOCAL
            lbl_pista_activa.value = "Pista: Ambient Synthesizer (Local Asset)"
        else:
            audio_player.src = AUDIO_MUSIC_REMOTE
            lbl_pista_activa.value = "Pista: Soundtrack Stream (Cloud URL)"
        audio_player.update()
        if is_playing:
            await audio_player.play()
        page.update()

    selector_fuente = ft.RadioGroup(
        content=ft.Row(
            [
                ft.Radio(value="local", label="Audio Local (assets/audio/)", fill_color="#58A6FF"),
                ft.Radio(value="cloud", label="Audio Cloud (URL MP3)", fill_color="#58A6FF"),
            ],
            spacing=20,
        ),
        value="local" if AUDIO_MUSIC_LOCAL else "cloud",
        on_change=cambiar_fuente_audio,
    )

    tarjeta_reproductor = ft.Container(
        content=ft.Column(
            [
                # Encabezado del reproductor
                ft.Row(
                    [
                        ft.Row(
                            [
                                ft.Container(
                                    content=ft.Icon(ft.Icons.MUSIC_NOTE_ROUNDED, color="#58A6FF", size=26),
                                    bgcolor="#1F2937",
                                    padding=10,
                                    border_radius=12,
                                    border=ft.Border.all(1, "#374151"),
                                ),
                                ft.Column(
                                    [
                                        ft.Text("Reproductor de Audio Continuo", size=17, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                        lbl_pista_activa,
                                    ],
                                    spacing=2,
                                ),
                            ],
                            spacing=12,
                        ),
                        ft.Row(
                            [
                                ft.Row(barras_ecualizador, spacing=3),
                                ft.Container(width=8),
                                badge_estado,
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(height=16, color="#21262D"),
                # Selector de fuente (Local vs Cloud)
                ft.Row(
                    [
                        ft.Text("Fuente de reproducción:", size=12, color="#8B949E", weight=ft.FontWeight.W_500),
                        selector_fuente,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                # Barra de progreso y tiempo
                ft.Column(
                    [
                        slider_progreso,
                        ft.Row(
                            [lbl_tiempo_actual, lbl_tiempo_total],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                    ],
                    spacing=2,
                ),
                # Botones de control y volumen
                ft.Row(
                    [
                        ft.Row(
                            [
                                btn_play_pause,
                                btn_stop,
                            ],
                            spacing=10,
                        ),
                        ft.Row(
                            [
                                btn_mute,
                                ft.Container(width=130, content=slider_volumen),
                                txt_volumen,
                            ],
                            spacing=6,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            spacing=14,
        ),
        padding=22,
        border_radius=16,
        bgcolor="#161B22",
        border=ft.Border.all(1, "#30363D"),
        shadow=ft.BoxShadow(blur_radius=12, color=ft.Colors.with_opacity(0.2, "#000000")),
    )

    # =========================================================================
    # GUÍA RÁPIDA: CLAVES DE AUDIO EN FLET 1.0.3
    # =========================================================================
    tarjeta_tips = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.TIPS_AND_UPDATES_ROUNDED, color="#E3B341", size=20),
                        ft.Text("¿Por qué no sonaba antes? Cambios en Flet 1.0.3", size=14, weight=ft.FontWeight.BOLD, color="#E3B341"),
                    ],
                    spacing=8,
                ),
                ft.Text(
                    "• Métodos Asíncronos: play(), pause(), resume() y seek() en flet_audio 1.0.3 son corrutinas. Si se llaman sin 'await', Python descarta la corrutina y nunca se emite sonido.\n"
                    "• ft.Service en vez de page.overlay: Audio ya no es un control visual para 'page.overlay'. Se registra directamente como servicio en la página.\n"
                    "• ReleaseMode.STOP para SFX: Evita que el reproductor libere y redescargue el archivo tras cada reproducción, logrando clics instantáneos sin lag.\n"
                    "• Soporte Dual (Local + Cloud): Configura ft.run(main, assets_dir='assets') y src='/audio/archivo.wav' para sonido garantizado incluso sin conexión.",
                    size=12,
                    color="#8B949E",
                ),
            ],
            spacing=8,
        ),
        padding=16,
        border_radius=12,
        bgcolor="#1C180B",
        border=ft.Border.all(1, "#4D3800"),
    )

    # =========================================================================
    # ENSAMBLADO GENERAL DE LA VISTA
    # =========================================================================
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    # Cabecera principal
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(ft.Icons.GRAPHIC_EQ_ROUNDED, color="#00E8C6", size=32),
                                bgcolor="#0A2222",
                                padding=12,
                                border_radius=14,
                                border=ft.Border.all(1, "#00E8C6"),
                            ),
                            ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Text("Flet Audio Studio", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                            ft.Container(
                                                content=ft.Text("v1.0.3 READY", size=10, weight=ft.FontWeight.BOLD, color="#00E8C6"),
                                                bgcolor="#0D2E28",
                                                padding=ft.Padding.symmetric(horizontal=8, vertical=3),
                                                border_radius=12,
                                                border=ft.Border.all(1, "#00E8C6"),
                                            ),
                                        ],
                                        spacing=10,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                    ft.Text(
                                        "Demostración de efectos sonoros (SFX), sincronización visual y reproductor continuo en Flet 1.0.3.",
                                        size=13,
                                        color="#8B949E",
                                    ),
                                ],
                                spacing=2,
                            ),
                        ],
                        spacing=16,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Divider(height=20, color="#21262D"),
                    # Subtítulo SFX
                    ft.Row(
                        [
                            ft.Text("1. EFECTOS DE SONIDO & FEEDBACK AUDITIVO", size=13, weight=ft.FontWeight.BOLD, color="#00E8C6"),
                            ft.Text("(ReleaseMode.STOP - Sin latencia)", size=11, color="#8B949E"),
                        ],
                        spacing=8,
                    ),
                    grid_sfx,
                    ft.Container(height=10),
                    # Subtítulo Reproductor
                    ft.Row(
                        [
                            ft.Text("2. REPRODUCTOR CONTINUO CON TIEMPO REAL", size=13, weight=ft.FontWeight.BOLD, color="#58A6FF"),
                            ft.Text("(ReleaseMode.LOOP - Progreso & Volumen)", size=11, color="#8B949E"),
                        ],
                        spacing=8,
                    ),
                    tarjeta_reproductor,
                    ft.Container(height=6),
                    # Caja informativa
                    tarjeta_tips,
                ],
                spacing=16,
            ),
            width=760,
        )
    )


if __name__ == "__main__":
    # Importante: assets_dir='assets' para resolver rutas '/audio/...'
    ft.run(main, assets_dir="assets")
