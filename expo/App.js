import { StatusBar } from 'expo-status-bar';
import React from 'react';
import { StyleSheet, Text, View, TextInput, TouchableOpacity } from 'react-native';



export default function App() {
  const [_, doNothing] = React.useState(0);
  const onLogInPress = () => doNothing(prevCount => prevCount + 1);
  const [usernameValue, onUsernameInput] = React.useState('username');
  const [passwordValue, onPasswordInput] = React.useState('password');
  return (
    <View style={styles.container}>
      <Text style={[styles.setFontSizeBig, styles.setColorRed]}> Welcome </Text>
      <View
      style={{
        marginTop:10,
        backgroundColor:"#CC6665",
        borderBottomColor: '#000000',
        width:250,
        borderRadius:50,
        borderBottomWidth: 1,
      }}>
      <TextInput
        editable
        multiline
        numberOfLines={1}
        maxLength={100}
        textContentType="emailAddress"
        color="#ffffCC"
        onChangeText={text => onUsernameInput(text)}
        value={usernameValue}        
        style={{padding: 10}}/>
      </View>
      <View
      style={{
        marginTop:10,
        backgroundColor:"#CC6666",
        borderBottomColor: '#000000',
        width:250,
        borderRadius:50,
        borderBottomWidth: 1,
      }}>
      <TextInput
        editable
        multiline
        numberOfLines={1}
        maxLength={100}
        textContentType="password"
        color="#ffffCC"
        onChangeText={text => onPasswordInput(text)}
        value={passwordValue}        
        style={{padding: 10}}/>
      </View>
      <TouchableOpacity style={styles.button} onPress={onLogInPress}>
        <Text>Log In</Text>
      </TouchableOpacity>
      <StatusBar style="inverted" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
    alignItems: 'center',
    justifyContent: 'center',
  },
  setFontSizeBig: {
    fontSize: 64,
    fontWeight : 'bold' 
  },
  setFontSizeSmall: {
    fontSize: 12,
    fontWeight: 'normal',
  },
  setColorRed: {
    color: '#A03232'
  },
  setColorIvory: {
    color: "#FFFFCC"
  },
  button: {
    marginTop: 10,
    width: 250,
    borderRadius: 50,
    textAlign: "center",
    textTransform: 'uppercasea',
    backgroundColor: '#669999',
    padding: 10,
  },
});