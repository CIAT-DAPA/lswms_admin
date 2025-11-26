# forecasts_admin.py

from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_required, current_user
from datetime import datetime
import csv
import io

# Ajusta estos imports a tu estructura real:
from ormWP import Waterpoint, SeasonalForecast, SubseasonalForecast, Probability

forecasts_bp = Blueprint('forecasts', __name__)


@forecasts_bp.route('/forecasts', methods=['GET'])
@login_required
def show_forecasts_import():
    """
    Shows the form to upload CSV for seasonal or subseasonal forecasts.
    """
    return render_template('forecasts_import.html')
    # En el template tendrás:
    # - select forecast_type (seasonal / subseasonal)
    # - input file (csv)
    # - submit button


@forecasts_bp.route('/forecasts/import', methods=['POST'])
@login_required
def import_forecasts():
    """
    Handles CSV upload and creates Seasonal or Subseasonal forecasts in MongoDB.
    """
    forecast_type = request.form.get('forecast_type')
    file = request.files.get('file')

    if not forecast_type or forecast_type not in ('seasonal', 'subseasonal'):
        flash("Please select a valid forecast type (seasonal or subseasonal).", "error")
        return redirect('/forecasts')

    if not file or file.filename == '':
        flash("Please upload a CSV file.", "error")
        return redirect('/forecasts')

    try:
        # Read CSV as text
        content = file.stream.read().decode('utf-8-sig')
        csv_file = io.StringIO(content)
        reader = csv.DictReader(csv_file)
    except Exception as e:
        flash(f"Error reading CSV file: {e}", "error")
        return redirect('/forecasts')

    created = 0
    errors = []

    for idx, row in enumerate(reader, start=2):  # start=2 because line 1 is header
        # Skip completely empty rows
        if not any(row.values()):
            continue

        try:
            if forecast_type == 'seasonal':
                _create_seasonal_from_row(row)
            else:  # subseasonal
                _create_subseasonal_from_row(row)

            created += 1
        except Exception as e:
            errors.append(f"Line {idx}: {e}")

    if created > 0:
        flash(f"{created} {forecast_type} forecast(s) imported successfully.", "success")
    else:
        flash("No forecasts were imported.", "warning")

    if errors:
        flash(f"Some rows could not be imported. Example: {errors[0]}", "error")

    return redirect('/forecasts')


def _get_waterpoint_or_raise(waterpoint_id: str) -> Waterpoint:
    wp = Waterpoint.objects(id=waterpoint_id).first()
    if not wp:
        raise ValueError(f"Waterpoint with id '{waterpoint_id}' not found")
    return wp


def _create_seasonal_from_row(row: dict) -> None:
    waterpoint_id = row.get('waterpoint_id')
    year = row.get('year')
    month = row.get('month')   # NEW
    measure = row.get('measure')
    lower = row.get('lower')
    normal = row.get('normal')
    upper = row.get('upper')

    if not (waterpoint_id and year and month and measure and lower and normal and upper):
        raise ValueError("Missing required columns for seasonal row")

    wp = _get_waterpoint_or_raise(waterpoint_id)

    probability = Probability(
        measure=measure,
        below=float(lower),
        normal=float(normal),
        above=float(upper),
    )

    seasonal = SeasonalForecast(
        year=int(year),
        month=int(month),   # NEW
        probabilities=probability,
        waterpoint=wp,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        created_by=str(getattr(current_user, "id", "")),
    )
    seasonal.save()


def _create_subseasonal_from_row(row: dict) -> None:
    """
    Expects a row with:
    waterpoint_id,year,month,week,measure,lower,normal,upper
    """
    waterpoint_id = row.get('waterpoint_id')
    year = row.get('year')
    month = row.get('month')
    week = row.get('week')
    measure = row.get('measure')
    lower = row.get('lower')
    normal = row.get('normal')
    upper = row.get('upper')

    if not (waterpoint_id and year and month and week and measure and lower and normal and upper):
        raise ValueError("Missing required columns for subseasonal row")

    wp = _get_waterpoint_or_raise(waterpoint_id)

    probability = Probability(
        measure=measure,
        below=float(lower),
        normal=float(normal),
        above=float(upper),
    )

    ssf = SubseasonalForecast(
        year=int(year),
        month=int(month),
        week=int(week),
        probabilities=probability,
        waterpoint=wp,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        created_by="test",
    )
    ssf.save()