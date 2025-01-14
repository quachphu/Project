import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Modal, Button, Switch } from 'react-native';
import * as Animatable from 'react-native-animatable';
import WrappedModal from '../../components/WrappedModel'; // Adjust the path based on your project structure

export default function AccountScreen() {

  const generateWrappedData = () => {
    return {
      mostVisitedLocations: [
        { location: "Portola", visits: 64 },
        { location: "De La Guerra", visits: 135 },
        { location: "Carillo", visits: 36 },
      ],
      mostPurchasedItems: [
        { item: "Steamed Broccoli & Cauliflower (vgn)", count: 64 },
        { item: "Black Beans (vgn)", count: 65 },
        { item: "Wheat Tortilla (vgn)", count: 135 },
      ],
    };
  };

  const [userInfo, setUserInfo] = useState({});
  const [modalVisible, setModalVisible] = useState(false);
  const [preferences, setPreferences] = useState({
    wants_v: 0,
    wants_vgn: 0,
    wants_w_nuts: 0,
  });
const [wrappedData, setWrappedData] = useState(generateWrappedData());
const [wrappedModalVisible, setWrappedModalVisible] = useState(false);

  const userId = 1; // Replace with the actual user ID

  useEffect(() => {
    const fetchUserInfo = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/user_info?id=${userId}`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setUserInfo(data);
        setPreferences({
          wants_v: data.wants_v,
          wants_vgn: data.wants_vgn,
          wants_w_nuts: data.wants_w_nuts,
        });
      } catch (error) {
        console.error('Error fetching user info:', error);
      }
    };

    fetchUserInfo();
  }, []);

  const handleUpdatePreferences = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/update_preferences`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id: userId, ...preferences }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const updatedData = await response.json();
      setUserInfo(updatedData);
      setModalVisible(false);
    } catch (error) {
      console.error('Error updating preferences:', error);
    }
  };

  const togglePreference = (key) => {
    setPreferences((prev) => ({
      ...prev,
      [key]: prev[key] === 1 ? 0 : 1,
    }));
  };

  

  return (
    <View style={styles.container}>
      <Animatable.View animation="fadeIn" duration={1000}>
        <View style={styles.header}>
          <Text style={styles.headerText}>Hi {userInfo.username}</Text>
          <Text style={styles.subHeaderText}>{userInfo.email}</Text>
        </View>
      </Animatable.View>

      
      <WrappedModal
        visible={wrappedModalVisible}
        onClose={() => setWrappedModalVisible(false)}
        data={wrappedData}
      />
      <ScrollView style={styles.menuContainer}>
      
        <TouchableOpacity style={styles.menuItem} onPress={() => setModalVisible(true)}>
          <Text style={styles.menuText}>Preferences</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.menuItem} onPress={() => setWrappedModalVisible(!wrappedModalVisible)}>
            <Text style={styles.menuText}>Your 2024 Wrapped</Text>
        </TouchableOpacity>
        
        <TouchableOpacity style={styles.menuItem}>
          <Text style={styles.menuText}>Help & Support</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.menuItem}>
          <Text style={styles.menuText}>Sign Out</Text>
        </TouchableOpacity>
      </ScrollView>
    
      <Modal
        animationType="slide"
        transparent={true}
        visible={modalVisible}
        onRequestClose={() => setModalVisible(false)}
      >
        <View style={styles.modalContainer}>
          <Text style={styles.modalTitle}>Update Preferences</Text>
          <View style={styles.preferenceContainer}>
            <View style={styles.preferenceRow}>
              <Text>Wants Vegetarian:</Text>
              <Switch
                value={preferences.wants_v === 1}
                onValueChange={() => togglePreference('wants_v')}
              />
            </View>
            <View style={styles.preferenceRow}>
              <Text>Wants Vegan:</Text>
              <Switch
                value={preferences.wants_vgn === 1}
                onValueChange={() => togglePreference('wants_vgn')}
              />
            </View>
            <View style={styles.preferenceRow}>
              <Text>Not Allgeric to Nuts:</Text>
              <Switch
                value={preferences.wants_w_nuts === 1}
                onValueChange={() => togglePreference('wants_w_nuts')}
              />
            </View>
          </View>
          <View style={styles.buttonContainer}>
            <Button title="Submit" onPress={handleUpdatePreferences} />
            <Button title="Close" onPress={() => setModalVisible(false)} />
          </View>
        </View>
      </Modal>


    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  header: {
    backgroundColor: '#003366',
    padding: 20,
    alignItems: 'flex-start',
  },
  headerText: {
    fontSize: 24,
    color: '#fff',
    fontWeight: 'bold',
  },
  subHeaderText: {
    fontSize: 16,
    color: '#fff',
  },
  menuContainer: {
    marginTop: 20,
  },
  menuItem: {
    padding: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#ccc',
  },
  menuText: {
    fontSize: 18,
  },
  modalContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#d3d3d3', // Light gray background
    padding: 20,
  },
  modalTitle: {
    fontSize: 24,
    color: '#000',
    marginBottom: 20,
  },
  preferenceContainer: {
    width: '100%',
    marginBottom: 20,
  },
  preferenceRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    width: '100%',
  },
});