extern crate rand;
use std::fs::File;
use std::io::{self, prelude::*, BufReader};
use std::str::FromStr;
use rand::distributions::{Distribution, Uniform};

const NUMDAYS:usize = 3254;
const TRAINSIZE:usize = 2765;
const TESTSIZE:usize = 489;

pub(crate) fn log_reg() -> io::Result<()> {
    let file = File::open("bitcoin_clean_rust.csv")?;
    let reader = BufReader::new(file);

	let mut x:[f64; NUMDAYS] = [0.0; NUMDAYS];
    let mut y:[f64; NUMDAYS] = [0.0; NUMDAYS];
	let mut x_test:[f64; NUMDAYS] = [0.0; NUMDAYS];
	let mut y_test:[f64; NUMDAYS] = [0.0; NUMDAYS];
	let mut i = 0;
	let mut j = 0;
	let mut flag = -1;
    for line in reader.lines() {
		if flag == -1{
			flag += 1;
			continue;
		}
		if i >= NUMDAYS{
			break;
		}
		if i < TRAINSIZE{
			for s in line?.split(","){
				//get weighted_price
				if j == 1{
					x[i] = f64::from_str(s).unwrap();
				}
				//get label
				if j == 2{
					y[i] = f64::from_str(s).unwrap();
				}
				j += 1;
			}
		}
		else{
			for s in line?.split(","){
				//get weighted_price
				if j == 1{
					x_test[i-TRAINSIZE] = f64::from_str(s).unwrap();
				}
				//get label
				if j == 2{
					y_test[i-TRAINSIZE] = f64::from_str(s).unwrap();
				}
				j += 1;
			}
		}
		j = 0;
		i += 1;
    }

	let mut w_b:[f64; 2] = [0.0; 2];
	let iterations:usize = 1000;
	simulated_annealing(&mut w_b, &mut x, &mut y, iterations, TRAINSIZE);

	let mut predicted_labels:[f64; NUMDAYS] = [0.0; NUMDAYS];

	predict(&mut predicted_labels, &mut w_b, &mut x, TRAINSIZE);
	let train_acc = calc_acc(&mut predicted_labels, &mut y, TRAINSIZE);

	predict(&mut predicted_labels, &mut w_b, &mut x_test, TESTSIZE);
	let test_acc = calc_acc(&mut predicted_labels, &mut y_test, TESTSIZE);

	println!("training accuracy = {}", train_acc);
	println!("testing accuracy = {}", test_acc);

    Ok(())
}

fn cost(x_train:&mut [f64; NUMDAYS], y_train:&mut [f64; NUMDAYS], w:f64,
	b:f64, len_x:usize) -> f64
{
	let mut cost:f64 = 0.0;
	let mut x:f64;
	let mut y:f64;
	for i in 0..len_x{
		x = x_train[i];
		y = y_train[i];
		let z = -w*x-b;
		let f = 1.0/(1.0+z.exp());
		cost += y*f.ln() + (1.0-y)*(1.0-f).ln();
	}
	return (-1.0/(len_x as f64))*cost;
}

fn move_uphill(delta_e:f64, t:f64) -> bool{
	let x:f64 = delta_e/t;
	let between = Uniform::from(0.0..1.0);
	let mut rng = rand::thread_rng();
	let p:f64 = between.sample(&mut rng);
	if p < x.exp(){
		return true;
	}
	else{
		return false;
	}
}

fn simulated_annealing(w_b:&mut [f64; 2], x_train:&mut [f64; NUMDAYS], y_train:&mut [f64; NUMDAYS],
	iterations:usize, len_x:usize)
{
	let between = Uniform::from(0.0..1.0);
    let mut rng = rand::thread_rng();
	w_b[0] = between.sample(&mut rng);
	w_b[1] = between.sample(&mut rng);
	
	let mut new_w:f64;
	let mut new_b:f64;
	let mut delta_e:f64;
	let mut t:f64 = 1.0;
	let d:f64 = 0.99;
	
	for _i in 0..iterations{
		t = t * d;
		if t == 0.0{
			return;
		}
		new_w = between.sample(&mut rng);
		new_b = between.sample(&mut rng);
		delta_e = cost(x_train, y_train, w_b[0], w_b[1], len_x) -
			cost(x_train, y_train, new_w, new_b, len_x);
		if delta_e > 0.0{
			w_b[0] = new_w;
			w_b[1] = new_b;
		}
		else{
			if move_uphill(delta_e, t){
				w_b[0] = new_w;
				w_b[1] = new_b;
			}
		}
	}
}

fn predict(predicted_labels:&mut [f64; NUMDAYS], w_b:&mut [f64; 2],
	x_train:&mut [f64; NUMDAYS], len_x:usize)
{
	let w:f64 = w_b[0];
	let b:f64 = w_b[1];
	let mut x:f64;
	let mut z:f64;
	let mut f:f64;
	for i in 0..len_x{
		x = x_train[i];
		z = -w*x-b;
		f = 1.0/(1.0+z.exp());
		if f >= 0.5{
			predicted_labels[i] = 1.0;
		}
		else{
			predicted_labels[i] = 0.0;
		}
	}
}

fn calc_acc(predicted_labels:&mut [f64; NUMDAYS], labels:&mut [f64; NUMDAYS],
	len_labels:usize) -> f64
{
	let mut total:f64 = 0.0;
	for i in 0..len_labels{
		if predicted_labels[i] == labels[i]{
			total += 1.0;
		}
	}
	return total/(len_labels as f64);
}
