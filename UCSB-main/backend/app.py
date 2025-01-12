from flask import Flask, jsonify, request
import psycopg2
from flask_cors import CORS
import getpass
from dotenv import load_dotenv
import os 


load_dotenv()  
openai_api_key = os.getenv("OPENAI_API_KEY")
from langchain_openai import ChatOpenAI




app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8081"}}) 

# Database connection configuration
db_config = {
    'dbname': 'gaucho',
    'user': 'postgres', 
    'password': 'root',  
    'host': 'localhost',  
    'port': 5432          
}

@app.route('/wait_time', methods=['GET'])
def get_current_wait_time():
    dining_hall = request.args.get('dining_hall')
    if not dining_hall:
        return jsonify({"error": "Dining hall is required"}), 400

    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # SQL query to get the average of the first 5 wait times
        query = """
        SELECT AVG(wait_time) 
        FROM (
            SELECT wait_time 
            FROM wait_time 
            WHERE dining_hall = %s
            ORDER BY timestamp DESC  -- Order by timestamp to get the first 5 entries
            LIMIT 5
        ) AS first_five_wait_times;
        """

        cursor.execute(query, (dining_hall.lower(),))
        average_wait_time = cursor.fetchone()[0] 

        return jsonify({"average_wait_time": average_wait_time}), 200

    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return jsonify({"error": "Database connection failed"}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/recommend', methods=['GET'])
def recommend_menu_items():
    try:
        # Fetch all menu items
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        query = "SELECT * FROM public.dining_hall_menu;"
        cursor.execute(query)
        items = cursor.fetchall()
        formatted_items = [
            f"{item[1]}: {item[4]} (Dining Hall: {item[1]}, Time: {item[3]})" 
            for item in items
        ]
        print(formatted_items)

        # Prepare the input for LangChain
        user_query = request.args.get('user_query') 
        user_id = request.args.get('user_id')
        daily_query_number = request.args.get('daily_query_number')
        print(f"User ID: {user_id}, User Query: {user_query}, Daily Query Number: {daily_query_number}")

        # Insert the user query into the database
        insert_query = "INSERT INTO queries (user_id, query_text, queries_today) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (user_id, user_query, daily_query_number))
        conn.commit() 

        model = ChatOpenAI(model="gpt-4o-mini")

        messages = [
        (
        "system",
                f"You are a helpful assistant that recommends initially only 2 menu items unless they ask for more. Keep it concise from the University of California Santa Barbara Menu Items from their three dining halls Portola, La De Guerra, or Carrillo . Present the information in a very clear manner as well showing at which dining hall and what the food is. Here are the menu item names: {', '.join(formatted_items)}.",        ),
        ("human", user_query),
        ]

        ai_msg = model.invoke(messages)
        recommendations = ai_msg.content 

        return jsonify(recommendations)

    except Exception as e:
        print(f"Error in recommendation: {e}")
        return jsonify({"error": "Recommendation failed"}), 500
    finally:
        cursor.close()  # Close the cursor
        conn.close()    # Close the connection
        
@app.route('/menu', methods=['GET'])
def get_menu_items():
    user_id = request.args.get('userId') 
    dining_hall = request.args.get('dining_hall')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # SQL query to fetch menu items based on user preferences
        query = """
        SELECT *
        FROM dining_hall_menu d
        JOIN users p ON TRUE
        WHERE 
            p.id = %s
            AND d.dining_hall = %s
            -- Nut allergy handling
            AND (CASE 
                WHEN p.wants_w_nuts = 0 THEN d.is_w_nuts = 0  -- Exclude all items with nuts for allergic users
                ELSE TRUE  -- Show all items for non-allergic users
            END)
            -- Combined vegan/vegetarian handling
            AND (
                CASE
                    WHEN p.wants_vgn = 1 THEN (d.is_vgn = 1 OR d.is_v = 1)  -- Show both vegan AND vegetarian items
                    WHEN p.wants_v = 1 THEN d.is_v = 1  -- Show only vegetarian items
                    ELSE TRUE  -- Show all items
                END
            )
        ORDER BY 
            d.food_station,
            d.item_name;
        """

        # Execute the query
        cursor.execute(query, (user_id, dining_hall))
        items = cursor.fetchall()

        # Get column names
        column_names = [desc[0] for desc in cursor.description]

        result = [dict(zip(column_names, row)) for row in items]

        return jsonify(result)  # Return items as JSON

    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return jsonify({"error": "Database connection failed"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/user_info', methods=['GET'])
def get_user_info():
    user_id = request.args.get('id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE id = %s;"
        
        cursor.execute(query, (user_id,))
        user_info = cursor.fetchone() 

        if user_info is None:
            return jsonify({"error": "User not found"}), 404

        column_names = [desc[0] for desc in cursor.description]
        user_data = dict(zip(column_names, user_info))

        return jsonify(user_data), 200

    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return jsonify({"error": "Database connection failed"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/menu', methods=['GET'])
def get_all_menu_items():
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        query = "SELECT * FROM dining_hall_menu;"
        
        cursor.execute(query)
        items = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]

        result = [dict(zip(column_names, row)) for row in items]

        return jsonify(result)  

    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return jsonify({"error": "Database connection failed"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/update_preferences', methods=['POST'])
def update_user_preferences():
    data = request.get_json()
    user_id = data.get('id')
    wants_v = data.get('wants_v')
    wants_vgn = data.get('wants_vgn')
    wants_w_nuts = data.get('wants_w_nuts')

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # SQL query to update user preferences
        query = """
        UPDATE users
        SET wants_v = %s, wants_vgn = %s, wants_w_nuts = %s
        WHERE id = %s;
        """
        
        # Execute the query
        cursor.execute(query, (wants_v, wants_vgn, wants_w_nuts, user_id))
        conn.commit()  # Commit the changes

        return jsonify({"message": "User preferences updated successfully"}), 200

    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return jsonify({"error": "Database connection failed"}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(port=5000)  # Run the Flask app on port 5000