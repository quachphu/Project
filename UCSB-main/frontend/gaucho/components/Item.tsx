import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, Image, TouchableOpacity } from 'react-native';
import CustomModal from './Modal';

const dining_halls = [
  { id: 1, name: 'Carillo', category: 'Dining', hours: '8 AM - 10 PM', image: require('../assets/images/carrillo.png') },
  { id: 2, name: 'De La Guerra', category: 'Dining', hours: '9 AM - 11 PM', image: require('../assets/images/de_la_guerra.png') },
  { id: 3, name: 'Portola', category: 'Dining', hours: '7 AM - 9 PM', image: require('../assets/images/portola.png') },
];

export default function ItemList() {
  const [modalVisible, setModalVisible] = useState(false);
  const [currentWaitTime, setCurrentWaitTime] = useState({});
  const [menuItems, setMenuItems] = useState([]);
  const [currentDiningHall, setCurrentDiningHall] = useState('');
  const userId = 1; // Replace with the actual user ID

  const fetchWaitTimes = async () => {
    const waitTimePromises = dining_halls.map(async (hall) => {
      const response = await fetch(`http://127.0.0.1:5000/wait_time?dining_hall=${hall.name}`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      return { name: hall.name, waitTime: data.average_wait_time || 0 }; // Default to 0 if no data
    });

    try {
      const waitTimes = await Promise.all(waitTimePromises);
      const waitTimeMap = {};
      waitTimes.forEach(({ name, waitTime }) => {
        waitTimeMap[name] = waitTime / 60;
      });
      setCurrentWaitTime(waitTimeMap);
    } catch (error) {
      console.error('Error fetching wait times:', error);
    }
  };

  useEffect(() => {
    // Fetch wait times initially
    fetchWaitTimes();

    // Set up interval to fetch wait times every 5 minutes (300000 milliseconds)
    const intervalId = setInterval(fetchWaitTimes, 300000);

    // Clear the interval on component unmount
    return () => clearInterval(intervalId);
  }, []);

  const openModal = async (itemId, diningHall) => {
    console.log(`Opening modal for item ID: ${itemId} in dining hall: ${diningHall}`); // Debugging log
    try {
      const response = await fetch(`http://127.0.0.1:5000/menu?userId=${userId}&dining_hall=${diningHall}`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setMenuItems(data);
      setModalVisible(true);
    } catch (error) {
      console.error('Error fetching menu items:', error);
    }
  };

  const closeModal = () => {
    setModalVisible(false);
  };

  const onPress = (item) => {
    setCurrentDiningHall(item.name); // Set the current dining hall
    openModal(item.id, item.name); // Pass the dining hall name to openModal
  };

  const formatWaitTime = (waitTime) => {
    if (waitTime < 1) {
      return 'No wait time';
    } else if (waitTime >= 1 && waitTime < 5) {
      return '0-5 minutes';
    } else if (waitTime >= 5 && waitTime < 10) {
      return 'Less than 10 minutes';
    } else if (waitTime >= 10 && waitTime < 15) {
      return 'Less than 15 minutes';
    }  else if (waitTime >= 20 ) {
      return "Don't go";
    } else {
      "Unknown"
    }
  };

  return (
    <View style={styles.container}>
      {dining_halls.map(item => (
        <TouchableOpacity key={item.id} style={styles.itemContainer} onPress={() => onPress(item)}>
          <View style={styles.topContainer}>
            <Image source={item.image} style={styles.image} />
            <View style={styles.waitTimeContainer}>
              <Text >Wait time: </Text>               
              <Text style={styles.waitTime} >{formatWaitTime(currentWaitTime[item.name])}  </Text>     
            </View>
          </View>
          <View style={styles.bottomContainer}>
            <View style={styles.restaurantInfo}>
              <Text style={styles.itemName}>{item.name}</Text>
              <Text style={styles.itemCategory}>{item.category}</Text>
            </View>
            <View style={styles.hoursContainer}>
              <Text>{item.hours}</Text>
            </View>
          </View>
        </TouchableOpacity>
      ))}
      <CustomModal visible={modalVisible} onClose={closeModal} waitTime={currentWaitTime[currentDiningHall] || 0} menuItems={menuItems} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 16,
  },
  itemContainer: {
    marginBottom: 12,
    padding: 10,
    borderWidth: 1,
    borderColor: '#083464',
    borderRadius: 10,
  },
  topContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  image: {
    width: 200,
    height: 120,
    borderRadius: 10,
  },
  waitTimeContainer: {
    justifyContent: 'center',
    alignItems: 'flex-start',
    padding: 30,
    fontSize: 40,
  },
  bottomContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 10,
  },
  restaurantInfo: {
    flex: 1,
  },
  hoursContainer: {
    justifyContent: 'center',
    alignItems: 'flex-end',
  },
  itemName: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  itemCategory: {
    fontSize: 14,
    color: '#666',
  },
  waitTime: {
    fontSize: 20,
    marginTop: 5,
  }
});