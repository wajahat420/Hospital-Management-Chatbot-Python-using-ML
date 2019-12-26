from flask import Flask, request, render_template,jsonify
app = Flask(__name__)
def do_something(text1,text2):
   print("hello")
   text1 = text1.upper()
   text2 = text2.upper()
   combine = text1 + text2
   return combine
@app.route("/get_req", methods=["GET"])
def send_answer():
    return "answer from python"
@app.route('/')
def home():
    print("working")
    return  render_template('chatbot.html')
@app.route('/join', methods=['GET','POST'])
def my_form_post():
    print("jajajajajaja")
    text1 = request.form['text1']
    #word = request.args.get('text1')
    text2 = request.form['text2']
    combine = do_something(text1,text2)
    result = {
        "output": combine
        
    }
    print("text1",text1,"text2",text2)
    print("output",result)
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)
print("jjjjjjjjjjj")
if __name__ == '__main__':
    app.run(debug=True)