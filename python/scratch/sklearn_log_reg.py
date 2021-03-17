
model = LogisticRegression()

def main():
    df = pd.read_csv('bitcoin.csv')
    labels = df[['labels']]
    df.drop(['Unnamed: 0', 'Timestamp', 'labels'], axis=1, inplace=True)
    features = df.iloc().values()

    model.fit(features, labels)
    predicted_classes = model.predict(features)
    accuracy = accuracy_score(feature.flatten(), predicted_classes)


if __name__ == '__main__':
	main() 