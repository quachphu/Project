import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, FlatList, StyleSheet, ImageBackground } from 'react-native';
import Entypo from '@expo/vector-icons/Entypo';

const Chatbot = () => {
  const [userQuery, setUserQuery] = useState('');
  const [chatHistory, setChatHistory] = useState<Array<{type: string, text: string}>>([]);
  const [NumberofDailyQueries, setNumberofDailyQueries] = useState(0);
  const actualUserId = 1;

  const handleSend = async () => {
    if (!userQuery) return;

    // Save user query to chat history
    const newChatHistory = [...chatHistory, { type: 'user', text: userQuery }];
    setChatHistory(newChatHistory);

    try {
      const newQueryCount = NumberofDailyQueries + 1;
      setNumberofDailyQueries(newQueryCount);

      console.log(`Fetching URL: http://127.0.0.1:5000/recommend?user_query=${encodeURIComponent(userQuery)}&user_id=${actualUserId}&daily_query_number=${newQueryCount}`);

      const response = await fetch(
        `http://127.0.0.1:5000/recommend?` + 
        `user_query=${encodeURIComponent(userQuery)}` +
        `&user_id=${actualUserId}` + 
        `&daily_query_number=${newQueryCount}`
      );
      
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();

      setChatHistory((prev) => [...prev, { type: 'bot', text: data }]);
    } catch (error) {
      console.error('Error fetching recommendation:', error);
      setChatHistory((prev) => [...prev, { type: 'bot', text: 'Error fetching response.' }]);
    }
    setUserQuery('');

  };

  return (
    <ImageBackground 
      source={require('../../assets/images/chat_background.png')} 
      style={styles.background}
      resizeMode="cover"
    >
      <View style={styles.iconContainer}>
        <Entypo name="chat" size={40} style={styles.entypo} color="white" />
        <Text style={styles.iconText}>What would you like to know?</Text>
      </View>
      <View style={styles.container}>
      <FlatList
        data={chatHistory}
        keyExtractor={(item, index) => index.toString()}
        renderItem={({ item }) => (
          <View style={item.type === 'user' ? styles.userMessage : styles.botMessage}>
            <Text style={styles.messageText}>{item.text}</Text>
          </View>
        )}
        contentContainerStyle={styles.chatContainer}
      />
      <TextInput
        style={styles.input}
        placeholder="I want to eat chicken..."
        value={userQuery}
        onChangeText={setUserQuery}
      />
      <TouchableOpacity style={styles.button} onPress={handleSend}>
        <Text style={styles.buttonText}>Send</Text>
      </TouchableOpacity>
    </View>
    </ImageBackground>
    
  );
};

const styles = StyleSheet.create({
  iconContainer: {
    alignItems: 'center',
    marginTop: 10,
    color: '#fff'
  },
  iconText:{
    marginTop: 10,
    fontSize: 20,
    color: '#fff',
  },
  entypo: {
    padding: 10,
    marginTop: 10,
    borderColor: '#fff',
    borderWidth: 2,
    borderRadius: 30,
    overflow: 'hidden',
  },
  container: {
    flex: 1,
    padding: 10,
    backgroundColor: 'transparent',
  },
  button: {
    backgroundColor: '#000',
    padding: 10,
    borderRadius: 5,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 5,
    padding: 10,
    marginBottom: 10,
    backgroundColor: 'white',
  },
  userMessage: {
    alignSelf: 'flex-end',
    backgroundColor: '#d1e7dd',
    borderRadius: 5,
    padding: 10,
    marginVertical: 5,
    maxWidth: '80%',
  },
  botMessage: {
    alignSelf: 'flex-start',
    backgroundColor: '#f8d7da',
    borderRadius: 5,
    padding: 10,
    marginVertical: 5,
    maxWidth: '80%',
  },
  messageText: {
    color: '#000',
  },
  background: {
    flex: 1,
  },
  chatContainer: {
    flexGrow: 1,
    justifyContent: 'flex-end',
    paddingBottom: 10,
  },
});

export default Chatbot;