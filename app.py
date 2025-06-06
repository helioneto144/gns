import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import logging
from config import Config
from database import Database

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db = Database()

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def resize_image(image_path, max_size=(800, 800)):
    """Resize image to reduce file size while maintaining aspect ratio"""
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if necessary (for PNG with transparency)
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Resize image
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save with optimization
            img.save(image_path, 'JPEG', quality=85, optimize=True)
            logger.info(f"Image resized and optimized: {image_path}")
            
    except Exception as e:
        logger.error(f"Error resizing image: {str(e)}")

@app.route('/')
def index():
    """Registration form page"""
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    """Handle member registration"""
    try:
        # Get form data
        name = request.form.get('name', '').strip()
        commander_name = request.form.get('commander_name', '').strip()
        phone = request.form.get('phone', '').strip()
        
        # Validation
        if not name:
            flash('Nome é obrigatório!', 'error')
            return redirect(url_for('index'))
        
        if not commander_name:
            flash('Nome do comandante é obrigatório!', 'error')
            return redirect(url_for('index'))
        
        # Check if commander name already exists
        if db.check_commander_name_exists(commander_name):
            flash('Nome do comandante já existe! Escolha outro nome.', 'error')
            return redirect(url_for('index'))
        
        # Handle file upload
        photo_filename = None
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename and Config.allowed_file(file.filename):
                # Generate unique filename
                file_extension = file.filename.rsplit('.', 1)[1].lower()
                photo_filename = f"{uuid.uuid4().hex}.{file_extension}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
                
                # Save file
                file.save(file_path)
                
                # Resize and optimize image
                resize_image(file_path)
                
                logger.info(f"Photo uploaded: {photo_filename}")
        
        # Create member in database
        member = db.create_member(
            name=name,
            commander_name=commander_name,
            phone=phone if phone else None,
            photo_filename=photo_filename
        )
        
        if member:
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('directory'))
        else:
            flash('Erro ao realizar cadastro. Tente novamente.', 'error')
            return redirect(url_for('index'))
            
    except Exception as e:
        logger.error(f"Error in registration: {str(e)}")
        flash('Erro interno do servidor. Tente novamente.', 'error')
        return redirect(url_for('index'))

@app.route('/directory')
def directory():
    """Member directory/wall page"""
    try:
        members = db.get_all_members()
        return render_template('directory.html', members=members)
    except Exception as e:
        logger.error(f"Error loading directory: {str(e)}")
        flash('Erro ao carregar diretório de membros.', 'error')
        return redirect(url_for('index'))

@app.route('/api/members')
def api_members():
    """API endpoint to get all members (for AJAX requests)"""
    try:
        members = db.get_all_members()
        return jsonify(members)
    except Exception as e:
        logger.error(f"Error in API members: {str(e)}")
        return jsonify({'error': 'Erro ao carregar membros'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
