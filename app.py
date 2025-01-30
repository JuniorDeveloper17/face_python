from flask import Flask, request, jsonify
import os
from deepface import DeepFace  

app = Flask(__name__)

def save_temp_image(file):
    try:
        temp_dir = './temp_images'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        temp_file_path = os.path.join(temp_dir, file.filename)
        file.save(temp_file_path)  
        
        return temp_file_path
    except Exception as e:
        print(f"Error saat menyimpan gambar: {e}")
        return None


@app.route('/compare_faces', methods=['POST'])
def compare_faces_route():
    try:
        # Pastikan dua file dikirim
        if 'image1' not in request.files or 'image2' not in request.files:
            return jsonify({"error": "Both image1 and image2 are required"}), 400
  
        img1_path = save_temp_image(request.files['image1'])
        img2_path = save_temp_image(request.files['image2'])
        
        if img1_path is None or img2_path is None:
            return jsonify({"error": "Error saving one or both images"}), 500
           
        result = DeepFace.verify(img1_path, img2_path, model_name="Facenet512",anti_spoofing=True)
        print(result)
        os.remove(img1_path)
        os.remove(img2_path)
        distance = result["distance"]

        accuracy_percentage = max(0, (1 - distance) * 100)  
        
        return jsonify({
            "match": result["verified"],
            "distance": distance,
            "accuracy_percentage": accuracy_percentage
        }), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
