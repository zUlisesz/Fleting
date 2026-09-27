import flet.testing as ftt


async def test_periodic_table_renders(flet_app: ftt.FletTestApp):
    """The app should render the migrated periodic table UI."""
    tester = flet_app.tester

    await tester.pump_and_settle()

    assert (await tester.find_by_text("TABLA PERIÓDICA ELEMENTAL")).count == 1
    assert (await tester.find_by_text("Buscar elemento...")).count == 1
