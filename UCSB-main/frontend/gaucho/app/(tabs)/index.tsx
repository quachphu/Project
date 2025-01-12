import { ImageBackground, StyleSheet, ScrollView, View } from 'react-native';
import ItemList from '@/components/Item';

export default function HomeScreen() {
  return (
    <View style={styles.container}>
      <ImageBackground
        source={require('../../assets/images/ucsb.png')}
        style={styles.background}
      />
      <ScrollView contentContainerStyle={styles.scrollContainer}>
      <View style={styles.logoContainer}>
          <ImageBackground
            source={require('../../assets/images/ucsb_logo.png')}
            style={styles.logo}
          />
        </View>
        <View style={styles.contentContainer}>
          <ItemList />
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  logoContainer: {
    alignItems: 'center', // Center the logo horizontally
  },
  logo: {
    width: 300, // Set the width of the logo
    height: 200, // Set the height of the logo
    resizeMode: 'cover',
    marginTop: 20 // Ensure the logo maintains its aspect ratio
  },
  background: {
    flex: 1,
    resizeMode: 'cover',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
  },
  contentContainer: {
    backgroundColor: 'white',
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
    overflow: 'hidden',
    padding: 16,
    marginTop: 50,
  },
  scrollContainer: {
    flexGrow: 1,
  },
});