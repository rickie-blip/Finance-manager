# app/routes/settings.py
from flask import Blueprint, render_template, request, redirect, session, flash
from app.db import connect_db

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/')

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        # Update preferences
        theme = request.form.get('theme')
        filter_pref = request.form.get('filter_preference')
        try:
            cursor.execute("""
                UPDATE users
                SET theme_mode = %s, preferred_filter = %s
                WHERE user_id = %s
            """, (theme, filter_pref, user_id))
            conn.commit()
            flash("Settings updated successfully", "success")
        except Exception as e:
            print("Settings update error:", e)
            flash("Error updating settings", "error")
        finally:
            conn.close()
        return redirect('/settings')
    
    # GET - Fetch current settings
    cursor.execute("SELECT username, theme_mode, preferred_filter FROM users WHERE user_id = %s", (user_id,))
    user_settings = cursor.fetchone()
    conn.close()

    return render_template('settings.html', user=user_settings)
